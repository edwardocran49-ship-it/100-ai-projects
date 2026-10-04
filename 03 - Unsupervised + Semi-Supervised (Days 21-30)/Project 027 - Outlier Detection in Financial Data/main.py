import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score,recall_score
from sklearn.preprocessing import StandardScaler
from download_data import ensure_dataset
PROJECT_TITLE="Outlier Detection in Financial Data"
def run_demo():
    df=pd.read_csv(ensure_dataset(),nrows=150000); X=StandardScaler().fit_transform(df.drop(columns="Class")); model=IsolationForest(n_estimators=150,contamination=float(df.Class.mean()),random_state=42,n_jobs=1).fit(X); pred=(model.predict(X)==-1).astype(int)
    return {"project":27,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"Credit Card Fraud Detection","records":len(df),"outliers":int(pred.sum()),"metrics":{"precision":round(float(precision_score(df.Class,pred,zero_division=0)),4),"recall":round(float(recall_score(df.Class,pred,zero_division=0)),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
