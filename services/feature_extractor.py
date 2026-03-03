def extract_features(url):
    url_length = len(url)
    at_symbol = url.count('@')
    dot_count = url.count('.')
    has_https = 1 if "https" in url else 0
    has_ip = 1 if any(char.isdigit() for char in url.split("//")[-1].split("/")[0]) else 0

    return url_length, at_symbol, dot_count, has_https, has_ip