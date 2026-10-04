"""Seasonal ARIMA forecast of daily Capital Bikeshare demand."""
import pandas as pd
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from download_data import ensure_dataset

PROJECT_TITLE = "Predict Bike Rentals with Time-Series Models"

def run_demo():
    hourly = pd.read_csv(ensure_dataset())
    daily = hourly.groupby("dteday", as_index=False)["cnt"].sum()
    daily["dteday"] = pd.to_datetime(daily["dteday"])
    series = daily.set_index("dteday")["cnt"].asfreq("D")
    split = len(series) - 30
    model = SARIMAX(
        series.iloc[:split],
        order=(1, 1, 1),
        seasonal_order=(1, 0, 1, 7),
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit(disp=False, maxiter=100)
    prediction = model.forecast(len(series) - split)
    actual = series.iloc[split:]
    seasonal_naive = series.shift(7).iloc[split:]
    return {"project": 12, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Bike Sharing in Washington D.C.", "records": len(series), "model": "seasonal ARIMA (SARIMA)", "metrics": {"mae_rentals": round(float(mean_absolute_error(actual, prediction)), 4), "seasonal_naive_mae": round(float(mean_absolute_error(actual, seasonal_naive)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
