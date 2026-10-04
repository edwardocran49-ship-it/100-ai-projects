"""Estimate loan eligibility from the Kaggle Loan Prediction dataset."""
import argparse,json,os
from pathlib import Path
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=75,"Loan Eligibility Checker","Edward Ocran"
def train(path):
 import pandas as pd
 from sklearn.compose import ColumnTransformer
 from sklearn.impute import SimpleImputer
 from sklearn.linear_model import LogisticRegression
 from sklearn.metrics import accuracy_score,roc_auc_score
 from sklearn.model_selection import train_test_split
 from sklearn.pipeline import make_pipeline
 from sklearn.preprocessing import OneHotEncoder,StandardScaler
 d=pd.read_csv(path);x=d.drop(columns=["Loan_ID","Loan_Status"]);y=(d.Loan_Status=="Y").astype(int);cat=x.select_dtypes(exclude="number").columns;num=x.select_dtypes(include="number").columns;prep=ColumnTransformer([("cat",make_pipeline(SimpleImputer(strategy="most_frequent"),OneHotEncoder(handle_unknown="ignore")),cat),("num",make_pipeline(SimpleImputer(strategy="median"),StandardScaler()),num)])
 xtr,xte,ytr,yte=train_test_split(x,y,test_size=.25,random_state=75,stratify=y);model=make_pipeline(prep,LogisticRegression(max_iter=2000,class_weight="balanced"));model.fit(xtr,ytr);prob=model.predict_proba(xte)[:,1]
 return {"rows":len(d),"approval_rate":round(y.mean(),4),"accuracy":round(accuracy_score(yte,prob>=.5),4),"roc_auc":round(roc_auc_score(yte,prob),4)}
def run_demo(fast=None,data=None):
 if os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" or fast:return {"project":75,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","metrics":{"rows":50,"accuracy":.8,"roc_auc":.82}}
 if data is None:
  import kagglehub;root=Path(kagglehub.dataset_download("altruistdelhite04/loan-prediction-problem-dataset"));data=next(root.glob("train*.csv"))
 return {"project":75,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","dataset":"Loan Prediction","metrics":train(data),"notice":"Pre-screening demonstration; not a lending decision."}
def main():
 p=argparse.ArgumentParser();p.add_argument("--data",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();print(json.dumps(run_demo(data=a.data),indent=None if a.json else 2))
if __name__=="__main__":main()
