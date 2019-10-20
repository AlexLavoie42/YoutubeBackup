import json
import os
import string
import unicodedata

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib
import googleapiclient
import pandas
import pytube

from api import ApiHandler


class Downloader:
    def __init__(self):
        self.stream = None
        self.api = ApiHandler()

    def get_video_stream(self, url, resolution, fps, codec):
        self.stream = pytube.YouTube(url).streams.filter(file_extension=codec,
                                                         res=resolution,
                                                         fps=fps).first()

    def save_video(self, path, name):
        if not os.path.exists(f"{path}\\{clean_filename(name)}"):
            os.mkdir(f"{path}\\{clean_filename(name)}")
        if self.stream is not None:
            self.stream.download(f"{path}\\{clean_filename(name)}", name)

    def save_video_data(self, url, path, name):
        if not os.path.exists(f"{path}\\{clean_filename(name)}"):
            os.mkdir(f"{path}\\{clean_filename(name)}")
        data = self.api.get_video_data(url.split("v=")[1])

        json_str = json.dumps(data.data)
        with open(f"{path}\\{clean_filename(name)}\\"
                  f"{clean_filename(name)}.json", "w+") as f:
            f.write(json_str)
        js = pandas.read_json(json_str, typ='series')
        js.to_csv(f"{path}\\{clean_filename(name)}\\{clean_filename(name)}.csv"
                  , header=True)


class DataFetcher:

    def __init__(self, resolution, fps, codec, folder):
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
        self.api = ApiHandler()

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


def clean_filename(filename, replace='_'):
    """
    Taken and modified from:
    https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
    """
    whitelist = "-_.() %s%s" % (string.ascii_letters, string.digits)
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).\
        encode('ASCII',
               'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > 255:
        print(
            "Warning, filename truncated because it was over 255."
            " Filenames may no longer be unique".format(
                255))
    return cleaned_filename[:255]


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
