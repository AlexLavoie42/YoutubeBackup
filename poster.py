from enum import Enum

from api import ChannelApi
from util import clean_filename
from util import open_video_info


class VideoPoster:
    """Handles posting videos to youtube channel."""

    class Privacy(Enum):
        PRIVATE = 'private',
        PUBLIC = 'public',
        UNLISTED = 'unlisted'

    def __init__(self, privacy: Privacy):
        self.api = ChannelApi()
        self.privacy = privacy

    def post_video(self, title, folder, video_extension):
        """
        Posts video to youtube channel.
        :param title: Video title.
        :param folder: Folder to get video data from.
        :param video_extension: Extension of video file.
        """
        print(f"Posting {title}")
        print(f"{folder}\\data.json")
        video_data = open_video_info(f"{folder}\\"
                                     f"data.json")
        print(f"{video_data}")
        video_path = f"{folder}\\"\
                     f"{clean_filename(title)}.{video_extension}"
        print(f"{video_path}")
        print(f"{self.privacy}")
        self.api.initialize_upload(video_data, video_path, self.privacy)
        print(f"Posted {title}")
