from urllib.parse import urlparse
import re

def extract_features(url):

    parsed=urlparse(url)

    features=[]

    features.append(len(url))

    features.append(url.count("."))

    features.append(url.count("-"))

    features.append(len(re.findall(r'\d',url)))

    features.append(1 if parsed.scheme=="https" else 0)

    keywords=["login","verify","secure","account","update","bank"]

    k=0

    for w in keywords:

        if w in url.lower():

            k+=1

    features.append(k)

    features.append(1 if "@" in url else 0)

    ip_pattern=r'\d+\.\d+\.\d+\.\d+'

    features.append(1 if re.search(ip_pattern,url) else 0)

    features.append(parsed.netloc.count("."))

    return features