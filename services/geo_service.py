import socket

def get_ip_location(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        ip = socket.gethostbyname(domain)
        return {"ip": ip}
    except:
        return {"ip": "unknown"}