import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np, pandas as pd
import tensorflow as tf
from sklearn.metrics import mean_squared_error
from download_data import ensure_dataset
PROJECT_TITLE="Autoencoder for Noise Reduction"
def run_demo():
    tf.keras.utils.set_random_seed(42)
    df=pd.read_csv(ensure_dataset(),nrows=6000); clean=df.iloc[:,1:].to_numpy(np.float32)/255; rng=np.random.default_rng(42); noisy=np.clip(clean+rng.normal(0,.35,clean.shape),0,1).astype("float32")
    split=5000
    model=tf.keras.Sequential([tf.keras.layers.Input(shape=(784,)),tf.keras.layers.Dense(128,activation="relu"),tf.keras.layers.Dense(64,activation="relu",name="encoder"),tf.keras.layers.Dense(128,activation="relu"),tf.keras.layers.Dense(784,activation="sigmoid")])
    model.compile(optimizer="adam",loss="mse")
    model.fit(noisy[:split],clean[:split],epochs=8,batch_size=128,validation_split=.1,verbose=0)
    restored=model.predict(noisy[split:],verbose=0).clip(0,1)
    before=mean_squared_error(clean[split:],noisy[split:]); after=mean_squared_error(clean[split:],restored)
    return {"project":22,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"MNIST","records":len(df),"model":"fully connected TensorFlow autoencoder","metrics":{"noisy_mse":round(float(before),5),"reconstructed_mse":round(float(after),5)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
