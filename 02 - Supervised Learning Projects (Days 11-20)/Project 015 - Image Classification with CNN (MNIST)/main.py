"""Train a convolutional neural network on MNIST images."""
import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score
from download_data import ensure_dataset

PROJECT_TITLE = "Image Classification with CNN (MNIST)"

def run_demo():
    tf.keras.utils.set_random_seed(42)
    df = pd.read_csv(ensure_dataset(), nrows=12000)
    y = df.iloc[:, 0].to_numpy()
    X = df.iloc[:, 1:].to_numpy(dtype=np.float32).reshape(-1, 28, 28, 1) / 255
    split = 10000
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(64, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(X[:split], y[:split], epochs=3, batch_size=128, validation_split=.1, verbose=0)
    pred = model.predict(X[split:], verbose=0).argmax(axis=1)
    return {"project": 15, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "MNIST", "records": len(df), "model": "two-layer TensorFlow CNN", "metrics": {"accuracy": round(float(accuracy_score(y[split:], pred)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
