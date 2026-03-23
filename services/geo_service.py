import requests
import socket
from urllib.parse import urlparse

def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc or parsed.path
    except:
        return url

def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return "Unknown"

def get_geo(url):
    try:
        domain = extract_domain(url)
        ip = resolve_ip(domain)

        if ip == "Unknown":
            raise Exception("IP not found")

        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()

        return {
            "ip": ip,
            "city": data.get("city", "Unknown"),
            "country": data.get("country", "Unknown"),
            "lat": data.get("lat", 0),
            "lon": data.get("lon", 0),
            "isp": data.get("isp", "Unknown"),
            "org": data.get("org", "Unknown")
        }

    except:
        return {
            "ip": "Unknown",
            "city": "Unknown",
            "country": "Unknown",
            "lat": 0,
            "lon": 0,
            "isp": "Unknown",
            "org": "Unknown"
        }