"""ARIMA temperature forecasting on Delhi daily climate records."""
import pandas as pd
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from download_data import ensure_dataset

PROJECT_TITLE = "Forecast Weather Using ARIMA"

def run_demo():
    df = pd.read_csv(ensure_dataset(), parse_dates=["date"]).sort_values("date")
    series = df.set_index("date").meantemp.astype(float)
    split = len(series) - 60
    fitted = SARIMAX(series.iloc[:split], order=(1, 1, 1), seasonal_order=(1, 0, 1, 7), enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
    prediction = fitted.forecast(60)
    weekly_naive = series.iloc[split - 7:-7].to_numpy()[-60:]
    return {"project": 13, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Daily Delhi Climate", "records": len(df), "model": "SARIMA(1,1,1)(1,0,1,7)", "metrics": {"mae_celsius": round(float(mean_absolute_error(series.iloc[split:], prediction)), 4), "weekly_naive_mae_celsius": round(float(mean_absolute_error(series.iloc[split:], weekly_naive)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
