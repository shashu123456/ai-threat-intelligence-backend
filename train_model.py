import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# LOAD DATASET
df = pd.read_csv("dataset/url_dataset.csv")  # or phishing.csv

# EXPECTED COLUMNS:
# url, label (0 = safe, 1 = phishing)

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

# CREATE FEATURES
X = df["url"].astype(str).apply(extract_features).tolist()
y = df["label"]

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# MODEL
model = RandomForestClassifier(n_estimators=150)
model.fit(X_train, y_train)

# SAVE
joblib.dump(model, "phishing_model.pkl")

print("✅ Model trained & saved")