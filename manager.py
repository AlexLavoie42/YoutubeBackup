import os

import poster
import scraper
from util import open_video_info


class VideoManager:
    def __init__(self, res="720p", fps=30,
                 extension="mp4", include_thumbnail=True,
                 folder=".\\data",
                 privacy=poster.VideoPoster.Privacy.UNLISTED):
        self.fetcher = scraper.DataFetcher(res, fps, extension,
                                           folder)
        self.poster = poster.VideoPoster(privacy)
        self.extension = extension

    def save_videos(self, url):
        if isinstance(self.fetcher, scraper.DataFetcher):
            try:
                self.fetcher.parse_url(url)
                self.fetcher.save_data()
            except ValueError:
                print(f"{url} is not a valid Youtube URL")

    def post_video(self, path):
        video = open_video_info(path)
        for w in [x[0] for x in os.walk(path)]:
            self.poster.post_video(video.data['Title'], w, self.extension)

    def login(self):
        self.fetcher.api.get_login()
        self.poster.api.get_login()

    def change_folder(self, folder):
        if folder is None:
            self.fetcher.folder = ".\\data"
        else:
            self.fetcher.folder = folder
