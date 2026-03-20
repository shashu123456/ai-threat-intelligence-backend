import whois
from datetime import datetime

def analyze_domain(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        w = whois.whois(domain)

        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]

        age_days = (datetime.now() - creation).days

        return {
            "domain_age": age_days,
            "registrar": w.registrar
        }
    except:
        return {"domain_age": 0, "registrar": "unknown"}