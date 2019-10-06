import scraper


class GUI:
    pass


class VideoHandler:
    def __init__(self, url):
        self.url = url
        self.fetcher = None

    def init_fetcher(self, res="720p", fps="30fps",
                     codec="mp4", include_thumbnail=True, folder="/Data"):
        self.fetcher = scraper.DataFetcher(res, fps, codec, include_thumbnail,
                                           folder)

    def save_videos(self, url):
        self.fetcher.parse_url(url)
