import numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from download_data import ensure_dataset
PROJECT_TITLE="Autoencoder for Noise Reduction"
def run_demo():
    df=pd.read_csv(ensure_dataset(),nrows=6000); clean=df.iloc[:,1:].to_numpy(np.float32)/255; rng=np.random.default_rng(42); noisy=np.clip(clean+rng.normal(0,.35,clean.shape),0,1)
    split=5000; model=PCA(n_components=48,random_state=42).fit(noisy[:split]); restored=model.inverse_transform(model.transform(noisy[split:])).clip(0,1)
    before=mean_squared_error(clean[split:],noisy[split:]); after=mean_squared_error(clean[split:],restored)
    return {"project":22,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"MNIST","records":len(df),"model":"linear autoencoder (PCA equivalence)","metrics":{"noisy_mse":round(float(before),5),"reconstructed_mse":round(float(after),5)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
