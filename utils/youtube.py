from urllib.parse import urlparse, parse_qs

def get_video_id(url):

    parsed = urlparse(url)

    if "youtube.com" in parsed.netloc:
        return parse_qs(parsed.query)["v"][0]

    if "youtu.be" in parsed.netloc:
        return parsed.path[1:]

    return None