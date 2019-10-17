import json
import os
import urllib.request

import pandas
import pytube


class Downloader:
    def __init__(self, api_key):
        self.stream = None
        self.api = ApiHandler(api_key)

    def get_video_stream(self, url, resolution, fps, codec):
        self.stream = pytube.YouTube(url).streams.filter(file_extension=codec,
                                                         res=resolution,
                                                         fps=fps).first()

    def save_video(self, path, name):
        if self.stream is not None:
            self.stream.download(path, name)

    def save_video_data(self, url, path, name):
        data = self.api.get_video_data(url.split("v=")[1])

        json_str = json.dumps(data.data)
        with open(f"{path}\\{name}.json", "w+") as f:
            f.write(json_str)
        js = pandas.read_json(f"{path}\\{name}.json", typ='series')
        js.to_csv(f"{path}\\{name}.csv", header=True)


class DataFetcher:

    def __init__(self, resolution, fps, codec, folder, api_key):
        self.codec = codec
        self.fps = fps
        self.res = resolution
        if folder is None:
            self.folder = ".\\data"
        else:
            self.folder = folder
        if not os.path.exists(folder):
            os.mkdir(folder)
        self.video_urls = []
        self.downloader = Downloader(api_key)
        self.api = ApiHandler(api_key)

    def parse_url(self, url):
        if "youtube.com" not in url:
            raise ValueError("'url' must be a valid youtube url")
        elif 'list' in url:
            playlist = pytube.Playlist(url)
            playlist.playlist_url = playlist.construct_playlist_url()
            playlist.populate_video_urls()
            for u in playlist.video_urls:
                u = u.replace("https", "http")
                u = u.replace("www.", "")
                self.video_urls.append(u)
        elif 'watch?' in url:
            self.video_urls.append(url)
        elif 'channel' in url or 'user' in url:
            if 'channel' in url:
                channel_id = url.split("channel/")[1]
                self.video_urls = self.api.get_videos_in_channel(channel_id)
            elif 'user' in url:
                channel_id = self.api.get_channel_id_from_user(
                    url.split("user/")[1])
                self.video_urls = self.api.get_videos_in_channel(channel_id)
        else:
            raise ValueError("Unrecognized youtube url")

    def save_data(self):
        for v in self.video_urls:
            self.downloader.get_video_stream(v, self.res, self.fps,
                                             self.codec)
            self.downloader.save_video(self.folder,
                                       self.downloader.stream.title)
            self.downloader.save_video_data(v, self.folder,
                                            self.downloader.stream.title)
        self.video_urls = []


class ApiHandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_videos_in_channel(self, channel_id):

        base_video_url = 'https://www.youtube.com/watch?v='
        base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

        first_url = base_search_url + \
                    f'key={self.api_key}&channelId={channel_id}' \
                    f'&part=snippet,id&order=date&maxResults=25'

        video_links = []
        url = first_url
        while True:
            inp = urllib.request.urlopen(url)
            resp = json.load(inp)

            for i in resp['items']:
                if i['id']['kind'] == "youtube#video":
                    video_links.append(base_video_url + i['id']['videoId'])

            try:
                next_page_token = resp['nextPageToken']
                url = first_url + '&pageToken={}'.format(next_page_token)
            except Exception as e:
                for a in e.args:
                    print(a)
            return video_links

    def get_channel_id_from_user(self, user):
        base_search_url = 'https://www.googleapis.com/youtube/v3/channels?'
        url = (base_search_url +
               f'key={self.api_key}&forUsername={user}&part=id')
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)

        return resp['items'][0]['id']

    def get_video_data(self, video_id):
        search_url = 'https://www.googleapis.com/youtube/v3/videos?key=' \
                     f'{self.api_key}&part=snippet'
        url = f"{search_url}&id={video_id}"
        inp = urllib.request.urlopen(url)
        data = json.load(inp)['items'][0]['snippet']

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
        return VideoInfo(title, description, tags, category, thumbnail_url,
                         url, comments, views, subscribers, likes, dislikes)


class VideoInfo:
    def __init__(self, title, description, tags, category,
                 thumbnail_url, url,
                 comments, views, subscribers, likes, dislikes):
        self.data = {
            'Title': title,
            'Description': description,
            'Tags': tags,
            'Category': category,
            'ThumbnailURL': thumbnail_url,
            'URL': url,
            'Comments': comments,
            'Views': views,
            'Subscribers': subscribers,
            'Likes': likes,
            'Dislikes': dislikes
        }
