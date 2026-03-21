import socket
from urllib.parse import urlparse

def get_domain_info(url):
    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)

        return {
            "domain": domain,
            "ip": ip,
            "age": "Unknown",
            "registrar": "Unknown"
        }
    except:
        return {}