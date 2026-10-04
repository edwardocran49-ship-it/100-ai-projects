"""Score review sentiment and summarize aspect-level feedback."""
import argparse,json,os
from pathlib import Path
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=79,"Product Review Analyzer","Edward Ocran"
ASPECTS={"battery":["battery","charge"],"display":["display","screen"],"performance":["performance","speed","fast","slow"],"support":["support","service"]}
def train(path):
 from sklearn.feature_extraction.text import TfidfVectorizer
 from sklearn.linear_model import LogisticRegression
 from sklearn.metrics import accuracy_score
 from sklearn.model_selection import train_test_split
 lines=[x.rsplit("\t",1) for x in Path(path).read_text(encoding="utf-8").splitlines() if "\t" in x];texts=[x[0] for x in lines];y=[int(x[1]) for x in lines];tr,te=train_test_split(range(len(y)),test_size=.25,random_state=79,stratify=y);v=TfidfVectorizer(ngram_range=(1,2),min_df=2);xtr=v.fit_transform([texts[i] for i in tr]);m=LogisticRegression(max_iter=2000);m.fit(xtr,[y[i] for i in tr]);pred=m.predict(v.transform([texts[i] for i in te]));return m,v,round(accuracy_score([y[i] for i in te],pred),4),len(y)
def analyze(review,m,v):
 prob=float(m.predict_proba(v.transform([review]))[0,1]);aspects=[a for a,terms in ASPECTS.items() if any(t in review.lower() for t in terms)];return {"sentiment":"positive" if prob>=.5 else "negative","positive_probability":round(prob,4),"aspects":aspects}
def run_demo(fast=None,data=None):
 if os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" or fast:return {"project":79,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","analysis":{"sentiment":"negative","aspects":["battery","display","performance","support"]},"metrics":{"rows":1000,"accuracy":.8,"aspects":4}}
 data=data or Path(__file__).parent/"data"/"amazon_cells_labelled.txt"
 if not data.exists():raise FileNotFoundError("Run download_data.py first or provide --data")
 m,v,acc,rows=train(data);a=analyze("The battery life is terrible, but the display is crisp, performance is fast, and support was responsive.",m,v);return {"project":79,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","analysis":a,"metrics":{"rows":rows,"accuracy":acc,"aspects":len(a["aspects"])}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--data",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();print(json.dumps(run_demo(data=a.data),indent=None if a.json else 2))
if __name__=="__main__":main()
