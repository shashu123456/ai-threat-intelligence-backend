from flask import Blueprint
from database import get_connection

soc_bp = Blueprint("soc",__name__)

@soc_bp.route("/events")

def events():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""

    SELECT url,prediction,risk_score,timestamp
    FROM scans
    ORDER BY timestamp DESC
    LIMIT 20

    """)

    rows=cursor.fetchall()

    conn.close()

    events=[]

    for r in rows:

        events.append({

            "url":r[0],
            "prediction":r[1],
            "risk":r[2],
            "time":str(r[3])

        })

    return {"events":events}