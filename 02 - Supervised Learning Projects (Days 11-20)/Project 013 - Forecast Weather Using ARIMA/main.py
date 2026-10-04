"""ARIMA temperature forecasting on Delhi daily climate records."""
import pandas as pd
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA
from download_data import ensure_dataset

PROJECT_TITLE = "Forecast Weather Using ARIMA"

def run_demo():
    df = pd.read_csv(ensure_dataset(), parse_dates=["date"]).sort_values("date")
    series = df.set_index("date").meantemp.astype(float)
    split = len(series) - 60
    fitted = ARIMA(series.iloc[:split], order=(5, 1, 1)).fit()
    prediction = fitted.forecast(60)
    return {"project": 13, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Daily Delhi Climate", "records": len(df), "metrics": {"mae_celsius": round(float(mean_absolute_error(series.iloc[split:], prediction)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
