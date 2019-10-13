import abc


class VideoGroup(abc.ABC):
    def __init__(self, videos):
        self.videos = videos


class Playlist(VideoGroup):
    pass


class Channel(VideoGroup):
    pass


class Video:
    def __init__(self, files, info):
        """
        :param files: list of 'VideoFile'
        :param info: list of 'VideoInfo'
        """
        self.files = files
        self.info = info


class VideoData:
    def __init__(self, path):
        """
        :param path: String containing file path
        """
        self.data_path = path
        self.data = {}
        super().__init__()


class VideoInfo(VideoData):
    def __init__(self, title, description, tags, category, thumbnail_url, url,
                 comments, views, subscribers, likes, dislikes, path):
        super().__init__(path)
        self.data = {
            'Title': title,
            'Description': description,
            'Tags': tags,
            'Category': category,
            'ThumbnailURL': thumbnail_url,
            'URL': url,
            'Comments': comments,
            'Views': views,
            'Subscribers': subscribers,
            'Likes': likes,
            'Dislikes': dislikes
        }
