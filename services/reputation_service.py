def check_reputation(url):
    score = 0

    if "login" in url or "verify" in url:
        score += 20

    if url.count('.') > 5:
        score += 20

    if "http://" in url:
        score += 20

    return score