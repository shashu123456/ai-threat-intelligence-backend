def reputation_score(url):

    score=0

    if "@" in url:
        score+=30

    if url.count("-")>3:
        score+=20

    if len(url)>70:
        score+=30

    return score