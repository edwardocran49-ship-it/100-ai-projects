import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score
from download_data import ensure_dataset
PROJECT_TITLE="Anomaly Detection in Server Logs"
def run_demo():
    series_path, labels_path=ensure_dataset(); df=pd.read_csv(series_path,parse_dates=["timestamp"])
    values=df.value.astype(float); features=pd.DataFrame({"value":values,"delta":values.diff().fillna(0),"rolling_mean":values.rolling(12,min_periods=1).mean(),"rolling_std":values.rolling(12,min_periods=1).std().fillna(0)})
    key="realAWSCloudwatch/ec2_cpu_utilization_5f5533.csv"; windows=json.loads(labels_path.read_text())[key]
    truth=pd.Series(False,index=df.index)
    for start,end in windows: truth |= df.timestamp.between(pd.Timestamp(start),pd.Timestamp(end))
    contamination=max(.001,min(.2,float(truth.mean())))
    model=IsolationForest(n_estimators=150,contamination=contamination,random_state=42,n_jobs=1).fit(features)
    pred=(model.predict(features)==-1).astype(int)
    return {"project":21,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"Numenta Anomaly Benchmark EC2 CPU","records":len(df),"anomaly_points":int(truth.sum()),"metrics":{"precision":round(float(precision_score(truth,pred,zero_division=0)),4),"recall":round(float(recall_score(truth,pred,zero_division=0)),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
