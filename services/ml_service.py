import pickle
import os
import random

MODEL_PATH = "phishing_model.pkl"

if os.path.exists(MODEL_PATH):
    model = pickle.load(open(MODEL_PATH, "rb"))
else:
    model = None

def analyze_url(url):
    # Simplified demo logic
    if "login" in url or "verify" in url:
        return "Phishing", 85.0, 8
    return "Safe", 90.0, 2