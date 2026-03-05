def explain_url(url):

    reasons=[]

    if "@" in url:
        reasons.append("Contains @ symbol")

    if url.count("-")>2:
        reasons.append("Too many hyphens")

    if len(url)>60:
        reasons.append("URL too long")

    if url.count(".")>4:
        reasons.append("Too many subdomains")

    return reasons