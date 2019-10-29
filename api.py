import os

import google_auth_oauthlib
import google_auth_oauthlib.flow
import googleapiclient
import googleapiclient.discovery

from data import VideoInfo


class ApiHandler:
    credentials = None

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
            tags += t+","
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

    @classmethod
    def get_oauth_perm(cls):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow\
            .from_client_secrets_file(client_secrets_file, scopes)
        if cls.credentials is None:
            cls.credentials = flow.run_local_server()
        return googleapiclient.discovery.build(
            api_service_name, api_version, credentials=cls.credentials)
