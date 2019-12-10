import json
import os

import pandas
import pytube

from api import RetrieverApi
from util import clean_filename, threaded


class VideoDownloader:
    """Handles the downloading of video files."""

    def __init__(self):
        self.stream = None
        self.api = RetrieverApi()

    def get_video_stream(self, url, resolution, fps, codec):
        """
        Gets video stream from PYTube.
        :param url: Video URL.
        :param resolution: Resolution to download video in.
        :param fps: FPS to download video in.
        :param codec: Codec to download video.
        """
        self.stream = pytube.YouTube(url).streams.filter(file_extension=codec,
                                                         res=resolution,
                                                         fps=fps).first()

    def save_video(self, path, name):
        """
        Saves video file.
        :param path: Path to save video to.
        :param name: Video name.
        """
        print("Saving Video File...")
        if not os.path.exists(f"{path}\\{clean_filename(name)}"):
            os.mkdir(f"{path}\\{clean_filename(name)}")
        if self.stream is not None:
            self.stream.download(f"{path}\\{clean_filename(name)}", name)
        print("Video File Saved!")

    def save_video_data(self, url, path, name):
        """
        Saves video data to CSV and JSON
        :param url: Video URL.
        :param path: Path to save data to.
        :param name: Video name.
        """
        print("Saving Video Data...")
        if not os.path.exists(f"{path}\\{clean_filename(name)}"):
            os.mkdir(f"{path}\\{clean_filename(name)}")
        data = self.api.get_video_data(url.split("v=")[1])

        json_str = json.dumps(data.data)
        with open(f"{path}\\{clean_filename(name)}\\"
                  f"data.json", "w+") as f:
            f.write(json_str)
        js = pandas.read_json(json_str, typ='series')
        js.to_csv(f"{path}\\{clean_filename(name)}\\{clean_filename(name)}.csv"
                  , header=True)
        print("Video Data Saved!")


class DataFetcher:
    """Class for parsing URLs & saving data."""

    def __init__(self, resolution, fps, codec, folder):
        """
        :param resolution: Resolution to save video in.
        :param fps: FPS to save video in.
        :param codec: Codec to save video in.
        :param folder: Folder to save video in.
        """
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
        self.downloader = VideoDownloader()
        self.api = RetrieverApi()

    def parse_url(self, url):
        """
        Parses URL and finds out which method to use.
        TODO: Do this properly.
        :param url: Video URL.
        """
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
        """Saves video data."""
        def __save_vid(s, v):
            print(f"Saving {v}...")
            s.downloader.get_video_stream(v, s.res, s.fps,
                                          s.codec)
            s.downloader.save_video(s.folder,
                                    s.downloader.stream.title)
            s.downloader.save_video_data(v, s.folder,
                                         s.downloader.stream.title)
            print(f"{v} Saved!")

        for v in self.video_urls:
            threaded(__save_vid(self, v))
