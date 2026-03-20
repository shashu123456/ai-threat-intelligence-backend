import arff
import pandas as pd

with open("Training Dataset.arff") as f:
    dataset = arff.load(f)

data = pd.DataFrame(dataset["data"])

data.to_csv("dataset/phishing.csv", index=False)

print("Dataset converted successfully.")