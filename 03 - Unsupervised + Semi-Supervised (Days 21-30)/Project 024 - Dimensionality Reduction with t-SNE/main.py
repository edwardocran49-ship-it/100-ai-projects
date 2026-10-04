from sklearn.datasets import load_digits
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
PROJECT_TITLE="Dimensionality Reduction with t-SNE"
def run_demo():
    data=load_digits(); X=StandardScaler().fit_transform(data.data); model=TSNE(n_components=2,perplexity=30,init="pca",learning_rate="auto",random_state=42,max_iter=750); embedded=model.fit_transform(X)
    return {"project":24,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"Optical Recognition of Handwritten Digits","records":len(X),"metrics":{"class_silhouette_2d":round(float(silhouette_score(embedded,data.target)),4),"kl_divergence":round(float(model.kl_divergence_),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
