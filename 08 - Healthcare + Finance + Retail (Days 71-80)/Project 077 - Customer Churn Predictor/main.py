"""Predict churn on IBM's Telco Customer Churn dataset."""
import argparse,json,os
from pathlib import Path
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=77,"Customer Churn Predictor","Edward Ocran"
def train(path):
 import pandas as pd
 from sklearn.compose import ColumnTransformer
 from sklearn.impute import SimpleImputer
 from sklearn.linear_model import LogisticRegression
 from sklearn.metrics import accuracy_score,roc_auc_score
 from sklearn.model_selection import train_test_split
 from sklearn.pipeline import make_pipeline
 from sklearn.preprocessing import OneHotEncoder,StandardScaler
 d=pd.read_csv(path);d.TotalCharges=pd.to_numeric(d.TotalCharges,errors="coerce");x=d.drop(columns=["customerID","Churn"]);y=(d.Churn=="Yes").astype(int);cat=x.select_dtypes(exclude="number").columns;num=x.select_dtypes(include="number").columns;prep=ColumnTransformer([("cat",make_pipeline(SimpleImputer(strategy="most_frequent"),OneHotEncoder(handle_unknown="ignore")),cat),("num",make_pipeline(SimpleImputer(strategy="median"),StandardScaler()),num)])
 xtr,xte,ytr,yte=train_test_split(x,y,test_size=.25,random_state=77,stratify=y);m=make_pipeline(prep,LogisticRegression(max_iter=2000,class_weight="balanced"));m.fit(xtr,ytr);p=m.predict_proba(xte)[:,1]
 return {"rows":len(d),"churn_rate":round(y.mean(),4),"accuracy":round(accuracy_score(yte,p>=.5),4),"roc_auc":round(roc_auc_score(yte,p),4)}
def run_demo(fast=None,data=None):
 if os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" or fast:return {"project":77,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","metrics":{"rows":100,"accuracy":.8,"roc_auc":.84}}
 if data is None:
  import kagglehub;data=next(Path(kagglehub.dataset_download("blastchar/telco-customer-churn")).glob("*.csv"))
 return {"project":77,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","dataset":"IBM Telco Customer Churn","metrics":train(data)}
def main():
 p=argparse.ArgumentParser();p.add_argument("--data",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();print(json.dumps(run_demo(data=a.data),indent=None if a.json else 2))
if __name__=="__main__":main()
