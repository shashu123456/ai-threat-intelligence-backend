import requests

OPENPHISH_FEED = "https://openphish.com/feed.txt"


def check_openphish(url):

    try:
        r = requests.get(OPENPHISH_FEED, timeout=5)
        feed = r.text.splitlines()

        if url in feed:
            return True

    except:
        pass

    return False


def get_ip_reputation():

    try:
        r = requests.get("http://ip-api.com/json")

        data = r.json()

        return {
            "ip": data.get("query"),
            "city": data.get("city"),
            "country": data.get("country"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
        }

    except:
        return None