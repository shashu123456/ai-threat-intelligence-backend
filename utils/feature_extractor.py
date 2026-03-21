import re
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)

    hostname = parsed.netloc

    return [
        len(url),                               # URL length
        url.count("."),                         # dots
        1 if url.startswith("https") else 0,    # HTTPS
        len(hostname),                          # domain length
        1 if re.search(r"login|verify|bank|secure", url) else 0,
        1 if "@" in url else 0,
        1 if "-" in hostname else 0
    ]