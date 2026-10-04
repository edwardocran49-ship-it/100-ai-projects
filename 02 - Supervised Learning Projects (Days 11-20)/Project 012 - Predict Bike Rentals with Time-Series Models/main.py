"""Bike-rental forecasting on hourly Capital Bikeshare observations."""
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from download_data import ensure_dataset

PROJECT_TITLE = "Predict Bike Rentals with Time-Series Models"

def run_demo():
    df = pd.read_csv(ensure_dataset()).sort_values(["dteday", "hr"])
    for lag in (1, 24, 168):
        df[f"lag_{lag}"] = df["cnt"].shift(lag)
    df = df.dropna()
    features = ["season", "yr", "mnth", "hr", "holiday", "weekday", "workingday", "weathersit", "temp", "atemp", "hum", "windspeed", "lag_1", "lag_24", "lag_168"]
    split = int(len(df) * .8)
    model = HistGradientBoostingRegressor(max_iter=150, random_state=42).fit(df[features].iloc[:split], df.cnt.iloc[:split])
    prediction = model.predict(df[features].iloc[split:])
    return {"project": 12, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Bike Sharing in Washington D.C.", "records": len(df), "metrics": {"mae_rentals": round(float(mean_absolute_error(df.cnt.iloc[split:], prediction)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
