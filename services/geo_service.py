import requests
import socket
from urllib.parse import urlparse

def get_geo(url):
    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)

        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()

        return {
            "ip": ip,
            "city": data.get("city", "Unknown"),
            "country": data.get("country", "Unknown"),
            "lat": data.get("lat", 0),
            "lon": data.get("lon", 0),
            "isp": data.get("isp", "Unknown")
        }

    except Exception as e:
        print("Geo error:", e)
        return {
            "ip": "Unknown",
            "city": "Unknown",
            "country": "Unknown",
            "lat": 0,
            "lon": 0,
            "isp": "Unknown"
        }