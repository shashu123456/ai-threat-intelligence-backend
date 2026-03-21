import joblib
import numpy as np
from utils.feature_extractor import extract_features

model = joblib.load("phishing_model.pkl")

def predict_url(url):
    try:
        features = extract_features(url)
        features = np.array(features).reshape(1, -1)

        pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]

        return pred, prob

    except Exception as e:
        print("ML Error:", e)
        return 0, 0.1