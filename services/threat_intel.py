import requests
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ABUSE_API_KEY = os.getenv("ABUSE_API_KEY")


def check_google_safe(url):
    try:
        endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"

        payload = {
            "client": {"clientId": "ai-threat", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }

        res = requests.post(endpoint, json=payload)
        return res.status_code == 200 and "matches" in res.json()

    except:
        return False


def check_abuse_ip(ip):
    try:
        if not ip or ip == "Unknown":
            return False

        url = "https://api.abuseipdb.com/api/v2/check"

        headers = {
            "Key": ABUSE_API_KEY,
            "Accept": "application/json"
        }

        params = {
            "ipAddress": ip,
            "maxAgeInDays": 90
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        score = data["data"]["abuseConfidenceScore"]

        return score > 50

    except:
        return False