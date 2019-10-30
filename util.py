import json
import string
import unicodedata

from data import VideoInfo


def clean_filename(filename, replace='_'):
    """
    Taken and modified from:
    https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
    """
    whitelist = "-_.() %s%s" % (string.ascii_letters, string.digits)
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).\
        encode('ASCII',
               'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > 255:
        print(
            "Warning, filename truncated because it was over 255."
            " Filenames may no longer be unique".format(
                255))
    return cleaned_filename[:255]


def open_video_info(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return VideoInfo(data=data)
