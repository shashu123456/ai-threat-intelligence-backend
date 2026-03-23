"""
Threat Intelligence Service.

Integrates Google Safe Browsing, AbuseIPDB, and VirusTotal.
Each integration is optional — if API keys are missing or calls fail,
results degrade gracefully and the engine notes the gap.
"""

import logging
import requests
from typing import Dict, Any

logger = logging.getLogger(__name__)
TIMEOUT = 5


class ThreatIntelService:
    def __init__(self, gsb_key: str = "", abuseipdb_key: str = "", vt_key: str = ""):
        self.gsb_key = gsb_key
        self.abuseipdb_key = abuseipdb_key
        self.vt_key = vt_key

    def check(self, url: str, ip: str = "") -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "flagged": False,
            "sources": [],
            "gsb": {},
            "abuseipdb": {},
            "virustotal": {},
        }

        if self.gsb_key:
            gsb = self._check_gsb(url)
            result["gsb"] = gsb
            if gsb.get("flagged"):
                result["flagged"] = True
                result["sources"].append("Google Safe Browsing")

        if self.abuseipdb_key and ip:
            abuse = self._check_abuseipdb(ip)
            result["abuseipdb"] = abuse
            if abuse.get("flagged"):
                result["flagged"] = True
                result["sources"].append("AbuseIPDB")

        if self.vt_key:
            vt = self._check_virustotal(url)
            result["virustotal"] = vt
            if vt.get("flagged"):
                result["flagged"] = True
                result["sources"].append("VirusTotal")

        if not result["sources"]:
            result["note"] = "No API keys configured — external checks skipped."

        return result

    # ── Google Safe Browsing ───────────────────────────────────────────────────

    def _check_gsb(self, url: str) -> Dict[str, Any]:
        endpoint = (
            f"[safebrowsing.googleapis.com](https://safebrowsing.googleapis.com/v4/threatMatches:find)"
            f"?key={self.gsb_key}"
        )
        body = {
            "client": {"clientId": "cybershield-cti", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION",
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}],
            },
        }
        try:
            resp = requests.post(endpoint, json=body, timeout=TIMEOUT)
            data = resp.json()
            flagged = bool(data.get("matches"))
            threat_types = (
                [m["threatType"] for m in data["matches"]] if flagged else []
            )
            return {"flagged": flagged, "threat_types": threat_types}
        except Exception as e:
            logger.warning(f"GSB check failed: {e}")
            return {"flagged": False, "error": str(e)}

    # ── AbuseIPDB ──────────────────────────────────────────────────────────────

    def _check_abuseipdb(self, ip: str) -> Dict[str, Any]:
        try:
            resp = requests.get(
                "[api.abuseipdb.com](https://api.abuseipdb.com/api/v2/check)",
                headers={
                    "Key": self.abuseipdb_key,
                    "Accept": "application/json",
                },
                params={"ipAddress": ip, "maxAgeInDays": 90, "verbose": True},
                timeout=TIMEOUT,
            )
            data = resp.json().get("data", {})
            score = data.get("abuseConfidenceScore", 0)
            return {
                "flagged": score > 25,
                "abuse_confidence_score": score,
                "total_reports": data.get("totalReports", 0),
                "country_code": data.get("countryCode", ""),
                "isp": data.get("isp", ""),
                "domain": data.get("domain", ""),
                "last_reported_at": data.get("lastReportedAt", ""),
            }
        except Exception as e:
            logger.warning(f"AbuseIPDB check failed: {e}")
            return {"flagged": False, "error": str(e)}

    # ── VirusTotal ─────────────────────────────────────────────────────────────

    def _check_virustotal(self, url: str) -> Dict[str, Any]:
        import base64

        url_id = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
        try:
            resp = requests.get(
                f"[virustotal.com](https://www.virustotal.com/api/v3/urls/{url_id})",
                headers={"x-apikey": self.vt_key},
                timeout=TIMEOUT,
            )
            if resp.status_code == 404:
                return {"flagged": False, "note": "URL not in VT database"}
            data = resp.json()
            stats = (
                data.get("data", {})
                .get("attributes", {})
                .get("last_analysis_stats", {})
            )
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            return {
                "flagged": malicious > 0 or suspicious > 2,
                "malicious": malicious,
                "suspicious": suspicious,
                "harmless": stats.get("harmless", 0),
                "undetected": stats.get("undetected", 0),
            }
        except Exception as e:
            logger.warning(f"VirusTotal check failed: {e}")
            return {"flagged": False, "error": str(e)}
