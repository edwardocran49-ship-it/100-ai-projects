import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MultiLabelBinarizer
from download_data import ensure_dataset
PROJECT_TITLE="Clustering Movie Genres with K-Means"
def run_demo():
    df=pd.read_csv(ensure_dataset()); labels=df.genres.fillna("(no genres listed)").str.split("|"); X=MultiLabelBinarizer().fit_transform(labels)
    clusters=KMeans(n_clusters=12,n_init=20,random_state=42).fit_predict(X)
    return {"project":23,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"MovieLens latest-small movies","records":len(df),"clusters":12,"metrics":{"silhouette":round(float(silhouette_score(X,clusters,sample_size=min(5000,len(df)),random_state=42)),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
