from sklearn.ensemble import IsolationForest
import numpy as np

model = IsolationForest(contamination=0.1)

training_data = np.random.rand(200, 3)

model.fit(training_data)


def detect_anomaly(risk_score, url_length, dot_count):

    X = [[risk_score, url_length, dot_count]]

    score = model.decision_function(X)[0]

    return float(score)