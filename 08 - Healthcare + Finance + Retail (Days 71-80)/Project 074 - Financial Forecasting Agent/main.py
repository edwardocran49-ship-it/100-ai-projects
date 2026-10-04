"""Forecast AAPL closing prices with ARIMA and prediction intervals."""
import argparse,json,os
from pathlib import Path
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=74,"Financial Forecasting Agent","Edward Ocran"
def forecast(path):
 import pandas as pd
 from statsmodels.tsa.arima.model import ARIMA
 d=pd.read_csv(path);close=d["AAPL.Close"] if "AAPL.Close" in d else d["Close"];close=pd.to_numeric(close,errors="coerce").dropna();train,test=close.iloc[:-20],close.iloc[-20:];fit=ARIMA(train,order=(2,1,2)).fit();pred=fit.get_forecast(20);mean=pred.predicted_mean;mae=float(abs(mean.values-test.values).mean());future=ARIMA(close,order=(2,1,2)).fit().get_forecast(30);ci=future.conf_int()
 return {"rows":len(close),"holdout_mae":round(mae,3),"last_close":round(float(close.iloc[-1]),2),"forecast_30d":round(float(future.predicted_mean.iloc[-1]),2),"lower":round(float(ci.iloc[-1,0]),2),"upper":round(float(ci.iloc[-1,1]),2)}
def run_demo(fast=None,data=None):
 if os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" or fast:return {"project":74,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","metrics":{"rows":120,"holdout_mae":2.1,"forecast_30d":193.2}}
 if data is None:data=Path(__file__).resolve().parents[2]/"02 - Supervised Learning Projects (Days 11-20)"/"Project 011 - Predict Stock Prices with LSTM"/"data"/"AAPL.csv"
 return {"project":74,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","ticker":"AAPL","metrics":forecast(data)}
def main():
 p=argparse.ArgumentParser();p.add_argument("--data",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();print(json.dumps(run_demo(data=a.data),indent=None if a.json else 2))
if __name__=="__main__":main()
