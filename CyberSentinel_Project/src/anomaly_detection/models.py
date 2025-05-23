# src/anomaly_detection/models.py

import json
import numpy as np
from keras.models import Sequential
from keras.layers import Dense


class AutoencoderModel:
    def __init__(self, input_dim):
        self.input_dim = input_dim
        self.model = Sequential(
            [
                Dense(16, activation="relu", input_shape=(input_dim,)),
                Dense(8, activation="relu"),
                Dense(16, activation="relu"),
                Dense(input_dim, activation="sigmoid"),
            ]
        )
        self.model.compile(optimizer="adam", loss="mse")

    def train(self, X_train, epochs=10, batch_size=32):
        self.model.fit(
            X_train, X_train, epochs=epochs, batch_size=batch_size, verbose=0
        )

    def get_reconstruction_error(self, X):
        X = np.array(X)
        X_pred = self.model.predict(X, verbose=0)
        mse = np.mean(np.power(X - X_pred, 2), axis=1)
        return mse


def parse_log_line(log_line):
    try:
        log_dict = json.loads(log_line)
        features = [
            len(log_dict.get("event_type", "")),
            int(log_dict.get("bytes_sent", 0)),
            int(log_dict.get("src_ip", "0.0.0.0").split(".")[-1]),
        ]
        return features
    except Exception:
        return None


# Instantiate and train the autoencoder
_autoencoder = AutoencoderModel(input_dim=3)
_dummy_train_data = np.array([[15, 200, 250], [20, 220, 100], [10, 180, 80]])
_autoencoder.train(_dummy_train_data)


def detect_anomalies(log_line, threshold=0.1):
    features = parse_log_line(log_line)
    if features is None:
        return []

    error = _autoencoder.get_reconstruction_error([features])[0]
    if error > threshold:
        return [
            {
                "message": f"Anomaly detected with reconstruction error {error:.4f}",
                "score": float(error),
            }
        ]
    return []
