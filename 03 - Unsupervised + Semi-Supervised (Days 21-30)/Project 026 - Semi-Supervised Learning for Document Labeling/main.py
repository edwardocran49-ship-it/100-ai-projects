import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from download_data import ensure_dataset
PROJECT_TITLE="Semi-Supervised Learning for Document Labeling"
def run_demo():
    df=pd.read_csv(ensure_dataset(),nrows=5000); truth=(df.sentiment=="positive").astype(int).to_numpy(); split=4000
    vectorizer=TfidfVectorizer(max_features=8000,stop_words="english"); X_pool=vectorizer.fit_transform(df.review.iloc[:split]); X_test=vectorizer.transform(df.review.iloc[split:])
    rng=np.random.default_rng(42); labeled=np.sort(rng.choice(split,size=400,replace=False)); unlabeled=np.setdiff1d(np.arange(split),labeled)
    model=LogisticRegression(max_iter=500).fit(X_pool[labeled],truth[labeled]); baseline=accuracy_score(truth[split:],model.predict(X_test))
    probs=model.predict_proba(X_pool[unlabeled]); confidence=probs.max(axis=1); selected=unlabeled[confidence>=.9]
    selection_rule="probability >= 0.90"
    if len(selected)==0:
        selected=unlabeled[np.argsort(confidence)[-200:]]
        selection_rule="top 200 confidence fallback"
    pseudo=model.predict(X_pool[selected])
    combined=np.concatenate([labeled,selected]); combined_y=np.concatenate([truth[labeled],pseudo]); model.fit(X_pool[combined],combined_y); final=accuracy_score(truth[split:],model.predict(X_test))
    return {"project":26,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"IMDb 50K Movie Reviews","records":len(df),"labeled_records":len(labeled),"pseudo_labeled_records":len(selected),"selection_rule":selection_rule,"model":"TF-IDF logistic-regression self-training","metrics":{"supervised_accuracy":round(float(baseline),4),"self_training_accuracy":round(float(final),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
