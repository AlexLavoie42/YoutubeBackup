import scraper


class GUI:
    pass


class VideoHandler:
    def __init__(self):
        self.fetcher = None

    def init_fetcher(self, res="720p", fps=30,
                     extension="mp4", include_thumbnail=True,
                     folder=".\\data"):
        self.fetcher = scraper.DataFetcher(res, fps, extension,
                                           folder)

    def save_videos(self, url):
        if isinstance(self.fetcher, scraper.DataFetcher):
            self.fetcher.parse_url(url)
            self.fetcher.save_data()


def main():
    handler = VideoHandler()
    handler.init_fetcher()
    in_ = input("Enter youtube video url:")
    while in_.lower() is not "quit" or "q":
        try:
            handler.save_videos(in_)
        except Exception as e:
            for a in e.args:
                print(a)
        finally:
            in_ = input("Enter youtube video url:")


if __name__ == '__main__':
    main()
