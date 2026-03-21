from datetime import datetime

def log_event(message):
    with open("soc_logs.txt", "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")