"""Sequence prediction on five years of adjusted AAPL closing prices."""
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from download_data import ensure_dataset

PROJECT_TITLE = "Predict Stock Prices with LSTM"

def _lstm_features(windows, hidden=12):
    rng = np.random.default_rng(42)
    wx = rng.normal(0, .35, (4 * hidden, 1))
    wh = rng.normal(0, .18, (4 * hidden, hidden))
    bias = np.zeros(4 * hidden)
    encoded = []
    for window in windows:
        h = np.zeros(hidden); c = np.zeros(hidden)
        for value in window:
            z = wx[:, 0] * value + wh @ h + bias
            f, i, o = (1 / (1 + np.exp(-part)) for part in np.split(z[:3 * hidden], 3))
            g = np.tanh(z[3 * hidden:])
            c = f * c + i * g
            h = o * np.tanh(c)
        encoded.append(h)
    return np.asarray(encoded)

def run_demo():
    path = ensure_dataset()
    frame = pd.read_csv(path)
    close = pd.to_numeric(frame["Close"], errors="coerce").dropna().to_numpy(dtype=float)
    scaled = (close - close.mean()) / close.std()
    lookback = 20
    X = np.asarray([scaled[i-lookback:i] for i in range(lookback, len(scaled))])
    y = scaled[lookback:]
    features = _lstm_features(X)
    split = int(len(y) * .8)
    model = Ridge(alpha=.5).fit(features[:split], y[:split])
    predicted = model.predict(features[split:]) * close.std() + close.mean()
    actual = y[split:] * close.std() + close.mean()
    return {"project": 11, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "AAPL adjusted daily prices", "records": len(close), "model": "LSTM feature encoder with fitted output layer", "metrics": {"mae_usd": round(float(mean_absolute_error(actual, predicted)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
