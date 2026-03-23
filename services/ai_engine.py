import joblib

# LOAD MODEL
model = joblib.load("phishing_model.pkl")

def extract_features(url):
    return [
        len(url),
        url.count('.'),
        url.count('@'),
        url.count('-'),
        url.count('https'),
        url.count('http'),
        1 if 'login' in url else 0,
        1 if 'secure' in url else 0
    ]

def predict_url(url):
    features = extract_features(url)

    pred = model.predict([features])[0]
    prob = model.predict_proba([features])[0][1]

    return pred, prob