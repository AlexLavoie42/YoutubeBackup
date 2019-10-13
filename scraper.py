import json
import os
import urllib.request

import pytube


class Scraper:
    pass


class Downloader:
    def __init__(self):
        self.stream = None

    def get_video_stream(self, url, resolution, fps, codec, inc_thumbnail):
        self.stream = pytube.YouTube(url).streams.filter(file_extension=codec,
                                                         res=resolution,
                                                         fps=fps).first()

    def save_video(self, path, name):
        if self.stream is not None:
            self.stream.download(path, name)


class DataFetcher:
    thumbnail_url = "https://img.youtube.com/vi/%s/0.jpg"

    def __init__(self, resolution, fps, codec, inc_thumbnail, folder):
        self.inc_thumb = inc_thumbnail
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
        self.downloader = Downloader()

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
                self.video_urls = self.get_videos_in_channel(channel_id)
            elif 'user' in url:
                raise NotImplementedError("User's are not implemented."
                                          " Use channel url instead")
        else:
            raise ValueError("Unrecognized youtube url")

    def save_data(self):
        for v in self.video_urls:
            print(v)
            self.downloader.get_video_stream(v, self.res, self.fps,
                                             self.codec, self.inc_thumb)
            self.downloader.save_video(self.folder,
                                       self.downloader.stream.title)
        self.video_urls = []

    @staticmethod
    def get_videos_in_channel(channel_id):
        api_key = "AIzaSyBE9XOvqMVmsc9o0el2Fc9yYBnxck8UqFM"

        base_video_url = 'https://www.youtube.com/watch?v='
        base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

        first_url = base_search_url + \
                    f'key={api_key}&channelId={channel_id}' \
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
            except Exception:
                break
        return video_links
