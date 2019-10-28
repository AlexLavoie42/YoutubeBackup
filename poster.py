import json

from api import ApiHandler


def open_video_info(folder, file_path):
    with open(file_path) as f:
        data = json.load(f)
    print(data)


class VideoPoster:

    def __init__(self):
        self.api = ApiHandler()
