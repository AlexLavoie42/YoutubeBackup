class VideoInfo:
    def __init__(self, title=None, description=None,
                 tags=None, category=None,
                 thumbnail_url=None, url=None,
                 comments=None, views=None, subscribers=None,
                 likes=None, dislikes=None, data=None):
        if data is None:
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
        else:
            self.data = data
