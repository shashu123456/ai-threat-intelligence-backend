import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect("database.db")

def save_scan_history(user, url, prediction, confidence, risk_score, ip):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans (user, url, prediction, confidence, risk_score, ip, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user, url, prediction, confidence, risk_score, ip, datetime.utcnow()))

    conn.commit()
    conn.close()

def get_scan_stats():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE prediction='Phishing'")
    phishing_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE prediction='Safe'")
    safe_count = cursor.fetchone()[0]

    conn.close()

    return {
        "total_scans": total_scans,
        "phishing_detected": phishing_count,
        "safe_urls": safe_count
    }