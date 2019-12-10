import os

import poster
import scraper
from util import open_video_info


class VideoManager:
    """Handles the saving and posting of videos."""

    def __init__(self, res="720p", fps=30,
                 extension="mp4", include_thumbnail=True,
                 folder=".\\data",
                 privacy=poster.VideoPoster.Privacy.UNLISTED):
        """
        :param res: Video resolution to save.
        :param fps: Video FPS to save.
        :param extension: Video extension to save.
        :param include_thumbnail: Include thumbnail in folder? TODO: Implement
        :param folder: Folder to save video & data in.
        :param privacy: Privacy to upload video as.
        """
        self.fetcher = scraper.DataFetcher(res, fps, extension,
                                           folder)
        self.poster = poster.VideoPoster(privacy)
        self.extension = extension

    def save_videos(self, url: str):
        """
        Save video for given URL.
        :param url: URL to video.
        :return:
        """
        if isinstance(self.fetcher, scraper.DataFetcher):
            try:
                self.fetcher.parse_url(url)
                self.fetcher.save_data()
            except ValueError:
                print(f"{url} is not a valid Youtube URL")

    def post_video(self, path):
        for w in [x[0] for x in os.walk(path)]:
            try:
                video = open_video_info(f"{w}/data.json")
                self.poster.post_video(video.data['Title'], w, self.extension)
            except FileNotFoundError:
                pass

    def login(self):
        self.fetcher.api.get_login()
        self.poster.api.get_login()

    def change_folder(self, folder):
        if folder is None:
            self.fetcher.folder = ".\\data"
        else:
            self.fetcher.folder = folder
