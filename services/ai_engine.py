import os
import pickle
import numpy as np
from utils.feature_extractor import extract_features

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "model", "phishing_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def scan_url(url):

    features = extract_features(url)

    features = np.array(features).reshape(1, -1)

    prediction = model.predict(features)[0]

    prob = model.predict_proba(features)[0][prediction]

    result = "phishing" if prediction == 1 else "safe"

    risk_score = int(prob * 100)

    return {
        "prediction": result,
        "confidence": round(prob, 2),
        "risk_score": risk_score,
    }