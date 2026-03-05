import requests

API_KEY="YOUR_API_KEY"

def check_ip(ip):

    url=f"https://api.abuseipdb.com/api/v2/check"

    headers={
    "Key":API_KEY,
    "Accept":"application/json"
    }

    params={"ipAddress":ip}

    r=requests.get(url,headers=headers,params=params)

    return r.json()

@scan_bp.route("/intel/ip")

def intel_ip():

    ip=request.args.get("ip")

    data=check_ip(ip)

    return data