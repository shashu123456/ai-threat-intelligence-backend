import requests

def check_openphish(url):
    try:
        data = requests.get("https://openphish.com/feed.txt").text
        return url in data
    except:
        return False

def check_phishtank(url):
    return "phish" in url  # mock

def threat_score(url):
    score = 0
    if check_openphish(url):
        score += 40
    if check_phishtank(url):
        score += 30
    return score