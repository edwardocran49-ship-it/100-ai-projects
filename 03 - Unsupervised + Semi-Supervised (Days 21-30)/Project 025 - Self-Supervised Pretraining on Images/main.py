import numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from download_data import ensure_dataset
PROJECT_TITLE="Self-Supervised Pretraining on Images"
def run_demo():
    df=pd.read_csv(ensure_dataset(),nrows=10000); y=df.iloc[:,0].to_numpy(); X=df.iloc[:,1:].to_numpy(np.float32)/255
    pca=PCA(n_components=64,random_state=42).fit(X[:8000]); train_idx=np.arange(0,8000,10); model=LogisticRegression(max_iter=300).fit(pca.transform(X[train_idx]),y[train_idx]); pred=model.predict(pca.transform(X[8000:]))
    return {"project":25,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"MNIST","records":len(X),"labeled_training_images":len(train_idx),"metrics":{"accuracy":round(float(accuracy_score(y[8000:],pred)),4),"variance_retained":round(float(pca.explained_variance_ratio_.sum()),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
