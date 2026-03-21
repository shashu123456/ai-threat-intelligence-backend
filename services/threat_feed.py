import requests

VT_API_KEY = "1b91857ab7a49c20655683a09c3da2b589b21af695e29317078b3bf4e4d1e192"

def check_threat_feeds(url):
    try:
        headers = {
            "x-apikey": VT_API_KEY
        }

        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )

        if response.status_code != 200:
            return False

        analysis_id = response.json()["data"]["id"]

        report = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers
        ).json()

        stats = report["data"]["attributes"]["stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)

        return (malicious + suspicious) > 0

    except Exception as e:
        print("Threat API Error:", e)
        return False