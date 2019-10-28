import json

from api import ApiHandler
from scraper import VideoInfo


def open_video_info(folder, file_path):
    try:
        with open(file_path) as f:
            data = json.load(f)
            return VideoInfo(data['Title'], data['Description'], data['Tags'],
                             data['Category'], data['ThumbnailURL'],
                             data['URL'], data['Comments'], data['Views'],
                             data['Subscribers'], data['Likes'], data['Likes'])
    except FileNotFoundError:
        print(f"Video File '{file_path}' not found")


class VideoPoster:

    def __init__(self):
        self.api = ApiHandler()

    def post_video(self, title, folder):
        pass
