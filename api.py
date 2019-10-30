import os
import random
import time

import google_auth_oauthlib
import google_auth_oauthlib.flow
import googleapiclient
import googleapiclient.discovery
import httplib2
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from data import VideoInfo


class ApiHandler:
    CREDENTIALS = None

    RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
    MAX_RETRIES = 10
    httplib2.RETRIES = 1

    def __init__(self):
        self.youtube = self.get_oauth_perm()

    def get_videos_in_channel(self, channel_id):

        base_video_url = 'https://www.youtube.com/watch?v='

        response = self.youtube.channels().list(
            id=channel_id, part='snippet,id', order='date', maxResults=100)
        video_links = []
        while True:
            data = response.execute()

            for i in data['items']:
                if i['id']['kind'] == "youtube#video":
                    video_links.append(base_video_url + i['id']['videoId'])

            try:
                next_page_token = data['nextPageToken']
                data = self.youtube.channels().list(
                    id=channel_id, part='snippet,id', order='date',
                    maxResults=100, pageToken=next_page_token
                )
            except Exception as e:
                for a in e.args:
                    print(a)
            return video_links

    def get_channel_id_from_user(self, user):
        resp = self.youtube.channels().list(forUsername=user, part='id')
        data = resp.execute()

        return data['items'][0]['id']

    def get_video_data(self, video_id):
        response = self.youtube.videos().list(id=video_id, part='snippet')
        data = response.execute()['items'][0]['snippet']

        title = data['title']
        description = data['description']
        tags = ''
        for t in data['tags']:
            tags += t + ","
        category = data['categoryId']
        thumbnail_url = data['thumbnails']['default']['url']
        url = f"youtube.com/watch?v={video_id}"
        comments = None
        views = None
        subscribers = None
        likes = None
        dislikes = None
        return VideoInfo(title, description, tags, category,
                         thumbnail_url, url, comments, views,
                         subscribers, likes, dislikes)

    def post_video(self, video_info, video_file_path):
        pass

    def initialize_upload(self, youtube, options):
        tags = None
        if options.keywords:
            tags = options.keywords.split(",")

        body = dict(
            snippet=dict(
                title=options.title,
                description=options.description,
                tags=tags,
                categoryId=options.category
            ),
            status=dict(
                privacyStatus=options.privacyStatus
            )
        )

        # Call the API's videos.insert method to create and upload the video.
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            # The chunksize parameter specifies the size of each chunk of data, in
            # bytes, that will be uploaded at a time. Set a higher value for
            # reliable connections as fewer chunks lead to faster uploads. Set a lower
            # value for better recovery on less reliable connections.
            #
            # Setting "chunksize" equal to -1 in the code below means that the entire
            # file will be uploaded in a single HTTP request. (If the upload fails,
            # it will still be retried where it left off.) This is usually a best
            # practice, but if you're using Python older than 2.6 or if you're
            # running on App Engine, you should set the chunksize to something like
            # 1024 * 1024 (1 megabyte).
            media_body=MediaFileUpload(options.file, chunksize=-1,
                                       resumable=True)
        )

        self.resumable_upload(insert_request)

    # This method implements an exponential backoff strategy to resume a
    # failed upload.
    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print(
                            "Video id '%s' was successfully uploaded." %
                            response['id'])
                    else:
                        exit(
                            "The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if e.resp.status in self.RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (
                        e.resp.status,
                        e.content)
                else:
                    raise
            except self.RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
                if retry > self.MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print(
                    "Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    @classmethod
    def get_oauth_perm(cls):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow \
            .from_client_secrets_file(client_secrets_file, scopes)
        if cls.CREDENTIALS is None:
            cls.CREDENTIALS = flow.run_local_server()
        return googleapiclient.discovery.build(
            api_service_name, api_version, credentials=cls.CREDENTIALS)
