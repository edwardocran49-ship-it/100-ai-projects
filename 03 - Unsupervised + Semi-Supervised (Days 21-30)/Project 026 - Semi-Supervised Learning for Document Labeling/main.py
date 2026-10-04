import numpy as np, pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.semi_supervised import LabelSpreading
from download_data import ensure_dataset
PROJECT_TITLE="Semi-Supervised Learning for Document Labeling"
def run_demo():
    df=pd.read_csv(ensure_dataset(),nrows=4000); truth=(df.sentiment=="positive").astype(int).to_numpy(); vectors=TfidfVectorizer(max_features=5000,stop_words="english").fit_transform(df.review); X=TruncatedSVD(50,random_state=42).fit_transform(vectors)
    rng=np.random.default_rng(42); labeled=rng.choice(len(df),size=400,replace=False); y=np.full(len(df),-1); y[labeled]=truth[labeled]; model=LabelSpreading(kernel="knn",n_neighbors=15,max_iter=30).fit(X,y); mask=y==-1
    return {"project":26,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"IMDb 50K Movie Reviews","records":len(df),"labeled_records":len(labeled),"metrics":{"unlabeled_accuracy":round(float(accuracy_score(truth[mask],model.transduction_[mask])),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
