class VideoInfo:
    def __init__(self, title, description, tags, category,
                 thumbnail_url, url,
                 comments, views, subscribers, likes, dislikes):
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