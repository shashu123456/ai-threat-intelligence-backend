from database import db, URLScan
from datetime import datetime

def get_cached_scan(url):

    scan = URLScan.query.filter_by(url=url).first()

    if scan:
        return {
            "prediction": scan.prediction,
            "confidence": scan.confidence,
            "risk_score": scan.risk_score
        }

    return None


def store_scan(url, result):

    record = URLScan(
        url=url,
        prediction=result["prediction"],
        confidence=result["confidence"],
        risk_score=result["risk_score"],
        timestamp=datetime.utcnow()
    )

    db.session.add(record)
    db.session.commit()