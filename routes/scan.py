import json
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from extensions import db, socketio, limiter
from models import ScanResult, ThreatLog
from services.ai_engine import AIEngine
from services.geo_service import GeoService
from services.threat_intel_service import ThreatIntelService

scan_bp = Blueprint("scan", __name__)
_ai = AIEngine()
_geo = GeoService()


@scan_bp.route("/scan", methods=["POST"])
@limiter.limit("30 per minute")
def scan_url():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Normalise
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # ── Step 1: emit progress ──────────────────────────────────────────────────
    _emit_log("info", f"[SCAN] Initialising scan for {url}")

    # ── Step 2: Feature extraction + ML ───────────────────────────────────────
    _emit_log("info", "[ML] Extracting URL features...")
    features = _ai.extract_features(url)
    prediction, confidence, risk_score, explanation = _ai.predict(url, features)
    _emit_log(
        "info" if prediction == "safe" else "warning",
        f"[ML] Prediction: {prediction.upper()} | Risk: {risk_score:.0f}/100",
    )

    # ── Step 3: Geo resolution ─────────────────────────────────────────────────
    _emit_log("info", "[GEO] Resolving domain to IP...")
    geo_data = _geo.resolve(url)
    ip_address = geo_data.get("ip", "")
    _emit_log("info", f"[GEO] IP: {ip_address} → {geo_data.get('country', 'Unknown')}")

    # ── Step 4: Threat intelligence ───────────────────────────────────────────
    _emit_log("info", "[INTEL] Querying threat intelligence feeds...")
    threat_svc = ThreatIntelService(
        gsb_key=current_app.config["GOOGLE_SAFE_BROWSING_KEY"],
        abuseipdb_key=current_app.config["ABUSEIPDB_KEY"],
        vt_key=current_app.config["VIRUSTOTAL_KEY"],
    )
    threat_data = threat_svc.check(url, ip_address)

    # Merge external threat score into risk
    if threat_data.get("flagged"):
        risk_score = min(100, risk_score + 15)
        _emit_log("warning", "[INTEL] URL flagged by external threat feed!")

    # ── Step 5: Persist ────────────────────────────────────────────────────────
    scan = ScanResult(
        user_id=current_user.id if current_user.is_authenticated else None,
        url=url,
        risk_score=round(risk_score, 2),
        prediction=prediction,
        confidence=round(confidence, 4),
        explanation=explanation,
        features_json=json.dumps(features),
        ip_address=ip_address,
        geo_data_json=json.dumps(geo_data),
        threat_data_json=json.dumps(threat_data),
    )
    db.session.add(scan)

    severity = _risk_to_severity(risk_score)
    log = ThreatLog(
        event_type="URL_SCAN",
        severity=severity,
        message=f"{prediction.upper()} detected: {url} (risk={risk_score:.0f})",
        source_ip=ip_address,
        target_url=url,
    )
    db.session.add(log)
    db.session.commit()

    # ── Step 6: Socket broadcast ───────────────────────────────────────────────
    result_payload = {
        **scan.to_dict(),
        "geo_data": geo_data,
        "threat_data": threat_data,
    }

    socketio.emit("scan_result", result_payload)
    socketio.emit("new_log", log.to_dict())

    if risk_score >= 80:
        socketio.emit(
            "high_risk_alert",
            {
                "url": url,
                "risk_score": risk_score,
                "message": f"CRITICAL THREAT DETECTED — Risk Score {risk_score:.0f}/100",
            },
        )
        _emit_log("critical", f"[ALERT] High-risk URL blocked: {url}")

    return jsonify(result_payload), 200


@scan_bp.route("/scans/recent", methods=["GET"])
def recent_scans():
    scans = (
        ScanResult.query.order_by(ScanResult.created_at.desc()).limit(50).all()
    )
    return jsonify([s.to_dict() for s in scans]), 200


# ── Helpers ────────────────────────────────────────────────────────────────────

def _emit_log(level: str, message: str):
    socketio.emit("scan_log", {"level": level, "message": message})


def _risk_to_severity(score: float) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    return "low"
