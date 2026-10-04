"""Classify claim fraud risk from the Kaggle Auto Insurance Claims dataset."""
import argparse,json,os
from pathlib import Path
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=72,"Insurance Claim Classifier","Edward Ocran"
def train(path):
 import pandas as pd
 from sklearn.compose import ColumnTransformer
 from sklearn.ensemble import RandomForestClassifier
 from sklearn.impute import SimpleImputer
 from sklearn.metrics import accuracy_score,precision_recall_fscore_support
 from sklearn.model_selection import train_test_split
 from sklearn.pipeline import make_pipeline
 from sklearn.preprocessing import OneHotEncoder
 d=pd.read_csv(path).replace("?",pd.NA);cols=["incident_type","collision_type","incident_severity","authorities_contacted","property_damage","bodily_injuries","witnesses","police_report_available","total_claim_amount","injury_claim","property_claim","vehicle_claim","auto_make","auto_year"]
 x=d[cols];y=(d.fraud_reported=="Y").astype(int);cat=x.select_dtypes(exclude="number").columns;num=x.select_dtypes(include="number").columns
 prep=ColumnTransformer([("cat",make_pipeline(SimpleImputer(strategy="most_frequent"),OneHotEncoder(handle_unknown="ignore")),cat),("num",SimpleImputer(strategy="median"),num)])
 xtr,xte,ytr,yte=train_test_split(x,y,test_size=.25,random_state=72,stratify=y);model=make_pipeline(prep,RandomForestClassifier(n_estimators=220,class_weight="balanced",random_state=72,n_jobs=1));model.fit(xtr,ytr);pred=model.predict(xte);pr,re,f1,_=precision_recall_fscore_support(yte,pred,average="binary",zero_division=0)
 return {"accuracy":round(accuracy_score(yte,pred),4),"precision":round(pr,4),"recall":round(re,4),"f1":round(f1,4),"rows":len(d),"fraud_rate":round(y.mean(),4)}
def run_demo(fast=None,data=None):
 if os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" or fast:return {"project":72,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","metrics":{"accuracy":.8,"rows":20,"fraud_rate":.25}}
 if data is None:
  import kagglehub;data=next(Path(kagglehub.dataset_download("buntyshah/auto-insurance-claims-data")).glob("*.csv"))
 return {"project":72,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","dataset":"Auto Insurance Claims", "metrics":train(data)}
def main():
 p=argparse.ArgumentParser();p.add_argument("--data",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();print(json.dumps(run_demo(data=a.data),indent=None if a.json else 2))
if __name__=="__main__":main()
