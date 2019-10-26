from api import ApiHandler


class VideoPoster:

    def __init__(self):
        self.api = ApiHandler()

    def open_video_info(self, folder, file_path):
        with open(file_path):
            pass
