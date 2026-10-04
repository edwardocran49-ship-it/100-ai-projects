"""Convolution-feature image classification on the original MNIST pixels."""
import numpy as np
import pandas as pd
from scipy.signal import convolve2d
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from download_data import ensure_dataset

PROJECT_TITLE = "Image Classification with CNN (MNIST)"

def _features(images):
    kernels = [np.array([[1,0,-1],[2,0,-2],[1,0,-1]]), np.array([[1,2,1],[0,0,0],[-1,-2,-1]])]
    rows = []
    for image in images:
        maps = [np.maximum(convolve2d(image, kernel, mode="valid"), 0) for kernel in kernels]
        pooled = [m.reshape(13,2,13,2).max(axis=(1,3)).ravel() for m in maps]
        rows.append(np.concatenate(pooled))
    return np.asarray(rows)

def run_demo():
    df = pd.read_csv(ensure_dataset(), nrows=12000)
    y = df.iloc[:, 0].to_numpy(); images = df.iloc[:, 1:].to_numpy(dtype=np.float32).reshape(-1, 28, 28) / 255
    X = _features(images)
    split = 10000
    model = SGDClassifier(loss="log_loss", max_iter=40, random_state=42, n_jobs=1).fit(X[:split], y[:split])
    return {"project": 15, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "MNIST", "records": len(df), "model": "convolution-ReLU-pooling classifier", "metrics": {"accuracy": round(float(accuracy_score(y[split:], model.predict(X[split:]))), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
