"""
Geo Service — resolves a URL to an IP address and fetches geolocation data.
Uses ip-api.com (free, no key required) with a fallback stub.
"""

import re
import socket
import logging
import requests
from urllib.parse import urlparse
from typing import Dict, Any

logger = logging.getLogger(__name__)

GEO_API = "[ip-api.com](http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,lat,lon,isp,org,as,query)"
TIMEOUT = 4  # seconds


class GeoService:
    def resolve(self, url: str) -> Dict[str, Any]:
        domain = self._extract_domain(url)
        ip = self._resolve_ip(domain)
        if not ip:
            return self._unknown_geo(domain)

        geo = self._fetch_geo(ip)
        return geo

    # ── Helpers ────────────────────────────────────────────────────────────────

    @staticmethod
    def _extract_domain(url: str) -> str:
        parsed = urlparse(url)
        host = parsed.netloc or parsed.path
        return host.split(":")[0].replace("www.", "").lower()

    @staticmethod
    def _resolve_ip(domain: str) -> str:
        # Already an IP?
        try:
            socket.inet_aton(domain)
            return domain
        except OSError:
            pass
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            logger.debug(f"Could not resolve domain: {domain}")
            return ""

    @staticmethod
    def _fetch_geo(ip: str) -> Dict[str, Any]:
        try:
            resp = requests.get(GEO_API.format(ip=ip), timeout=TIMEOUT)
            data = resp.json()
            if data.get("status") == "success":
                return {
                    "ip": data.get("query", ip),
                    "country": data.get("country", "Unknown"),
                    "country_code": data.get("countryCode", ""),
                    "region": data.get("regionName", ""),
                    "city": data.get("city", ""),
                    "lat": data.get("lat", 0.0),
                    "lon": data.get("lon", 0.0),
                    "isp": data.get("isp", ""),
                    "org": data.get("org", ""),
                    "as": data.get("as", ""),
                }
        except Exception as e:
            logger.warning(f"Geo lookup failed for {ip}: {e}")

        return GeoService._unknown_geo(ip)

    @staticmethod
    def _unknown_geo(identifier: str) -> Dict[str, Any]:
        return {
            "ip": identifier,
            "country": "Unknown",
            "country_code": "",
            "region": "",
            "city": "",
            "lat": 0.0,
            "lon": 0.0,
            "isp": "",
            "org": "",
            "as": "",
        }
