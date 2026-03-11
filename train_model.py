import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
import os

# create model folder if not exists
if not os.path.exists("model"):
    os.makedirs("model")

data = {
    "url_length":[20,100,35,120,45,80],
    "num_dots":[1,4,2,5,1,3],
    "num_hyphens":[0,3,1,4,0,2],
    "num_special_chars":[2,10,3,12,2,7],
    "entropy":[2.1,4.5,2.5,4.8,2.3,3.9],
    "domain_length":[10,30,12,40,15,25],
    "num_subdomains":[0,2,0,3,0,1],
    "suspicious_words":[0,1,0,1,0,1],
    "has_ip":[0,1,0,1,0,1],
}

X = pd.DataFrame(data)

y = [0,1,0,1,0,1]

model = RandomForestClassifier()

model.fit(X,y)

with open("model/phishing_model.pkl","wb") as f:
    pickle.dump(model,f)

print("✅ phishing_model.pkl created successfully")