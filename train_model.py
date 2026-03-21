import pandas as pd
from xgboost import XGBClassifier
import pickle

df = pd.read_csv("dataset.csv")

X = df.drop("label", axis=1)
y = df["label"]

model = XGBClassifier()
model.fit(X, y)

pickle.dump(model, open("phishing_model.pkl", "wb"))

print("Model trained successfully")