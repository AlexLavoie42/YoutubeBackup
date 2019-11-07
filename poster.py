from api import ApiHandler
from util import clean_filename
from util import open_video_info


class VideoPoster:

    def __init__(self):
        self.api = ApiHandler()

    def post_video(self, title, folder, video_extension):
        video_data = open_video_info(f"{folder}\\{clean_filename(title)}\\"
                                     f"{clean_filename(title)}.json")
        video_path = f"{folder}\\{clean_filename(title)}\\"\
                     f"{clean_filename(title)}.{video_extension}"

