import pickle
import pandas as pd
from config import Config
from services.feature_extractor import extract_features

model = pickle.load(open(Config.MODEL_PATH, "rb"))

def analyze_url(url):
    url_length, at_symbol, dot_count, has_https, has_ip = extract_features(url)

    features = pd.DataFrame(
        [[url_length, at_symbol, dot_count, has_https, has_ip]],
        columns=["url_length", "at_symbol", "dot_count", "has_https", "has_ip"]
    )

    result = model.predict(features)[0]
    prob = model.predict_proba(features)[0]
    confidence = round(max(prob) * 100, 2)

    risk_score = (
        (url_length > 70) +
        (at_symbol > 0) +
        (dot_count > 5) +
        (has_https == 0) +
        (has_ip == 1)
    )

    if result == 1 or risk_score >= 2:
        prediction = "Phishing"
    else:
        prediction = "Safe"

    return prediction, confidence, risk_score