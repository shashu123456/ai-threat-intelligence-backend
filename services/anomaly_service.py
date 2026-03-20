from sklearn.ensemble import IsolationForest
import numpy as np

training_data = np.random.rand(200,5)

model = IsolationForest(contamination=0.1)
model.fit(training_data)


def detect_anomaly(features):

    features = np.array(features).reshape(1,-1)

    prediction = model.predict(features)

    return prediction[0] == -1