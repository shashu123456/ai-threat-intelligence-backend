import pickle
import numpy as np

model = pickle.load(open("model/phishing_model.pkl", "rb"))

def extract_features(url):
    return [
        len(url),
        url.count('.'),
        1 if "https" in url else 0,
        1 if "login" in url or "verify" in url else 0,
        len(url.split("//")[-1])
    ]

def predict_url(url):
    features = np.array(extract_features(url)).reshape(1, -1)
    pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]

    return pred, int(prob * 100)