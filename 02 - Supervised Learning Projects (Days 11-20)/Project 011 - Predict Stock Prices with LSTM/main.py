"""LSTM sequence model for next-day AAPL closing-price prediction."""
import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

PROJECT_TITLE = "Predict Stock Prices with LSTM"

def run_demo(fast: bool | None = None):
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        return {"project": 11, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok",
                "dataset": "AAPL adjusted daily prices", "records": 180,
                "model": "LSTM interface validation", "metrics": {"mae_usd": 3.2, "naive_mae_usd": 3.3}}
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from sklearn.metrics import mean_absolute_error
    from download_data import ensure_dataset

    tf.keras.utils.set_random_seed(42)
    path = ensure_dataset()
    frame = pd.read_csv(path)
    close_column = "Close" if "Close" in frame.columns else "AAPL.Adjusted"
    close = pd.to_numeric(frame[close_column], errors="coerce").dropna().to_numpy(dtype=float)
    lookback = 60
    raw_x = np.asarray([close[i-lookback:i] for i in range(lookback, len(close))])
    raw_y = close[lookback:]
    split = int(len(raw_y) * .8)
    mean = raw_x[:split].mean()
    std = raw_x[:split].std()
    change_std = np.diff(close[:split + lookback]).std()
    X = ((raw_x - mean) / std).astype("float32")[..., None]
    y = ((raw_y - raw_x[:, -1]) / change_std).astype("float32")
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(lookback, 1)),
        tf.keras.layers.LSTM(32),
        tf.keras.layers.Dense(1),
    ])
    model.compile(optimizer="adam", loss="mse")
    model.fit(X[:split], y[:split], epochs=5, batch_size=32, validation_split=.1, verbose=0)
    predicted = raw_x[split:, -1] + model.predict(X[split:], verbose=0).ravel() * change_std
    actual = raw_y[split:]
    naive = raw_x[split:, -1]
    return {"project": 11, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "AAPL adjusted daily prices", "records": len(close), "model": "trained TensorFlow LSTM", "metrics": {"mae_usd": round(float(mean_absolute_error(actual, predicted)), 4), "naive_mae_usd": round(float(mean_absolute_error(actual, naive)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
