import re
import math
from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login","verify","bank","account","secure","update","password"
]

def entropy(string):
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob])

def extract_features(url):

    parsed = urlparse(url)
    domain = parsed.netloc

    features = {}

    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")
    features["num_special_chars"] = len(re.findall(r"[^\w]", url))
    features["entropy"] = entropy(url)

    features["domain_length"] = len(domain)
    features["num_subdomains"] = domain.count(".") - 1

    features["suspicious_words"] = sum(word in url for word in SUSPICIOUS_WORDS)

    features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0

    return list(features.values())