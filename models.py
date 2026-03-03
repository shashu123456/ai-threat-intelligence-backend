from database import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE,
        password BYTEA,
        role VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id SERIAL PRIMARY KEY,
        user_email VARCHAR(255),
        url TEXT,
        prediction VARCHAR(50),
        confidence FLOAT,
        risk_score INT,
        ip VARCHAR(100),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def save_scan(user_email, url, prediction, confidence, risk_score, ip):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO scans (user_email, url, prediction, confidence, risk_score, ip)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_email, url, prediction, confidence, risk_score, ip))

    conn.commit()
    conn.close()