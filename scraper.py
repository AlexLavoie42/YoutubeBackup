import pytube


class Scraper:
    pass


class Downloader:
    def __init__(self):
        self.stream = None

    def get_video_stream(self, url, resolution, fps, codec, inc_thumbnail):
        pass

    def save_video(self, path):
        if self.stream is not None:
            pass


class DataFetcher:
    video_url = "https://img.youtube.com/vi/%s/0.jpg"

    def __init__(self, resolution, fps, codec, inc_thumbnail, folder):
        self.inc_thumb = inc_thumbnail
        self.codec = codec
        self.fps = fps
        self.res = resolution
        self.folder = folder

    def parse_url(self, url):
        pass

    def save_data(self):
        pass
