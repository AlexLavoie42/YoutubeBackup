import os

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
            # TODO: implement channels
            raise NotImplementedError("Channels not yet implemented")
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
