import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np, pandas as pd
import tensorflow as tf
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from download_data import ensure_dataset
PROJECT_TITLE="Self-Supervised Pretraining on Images"
def run_demo():
    tf.keras.utils.set_random_seed(42)
    df=pd.read_csv(ensure_dataset(),nrows=10000); y=df.iloc[:,0].to_numpy(); X=df.iloc[:,1:].to_numpy(np.float32).reshape(-1,28,28,1)/255
    rng=np.random.default_rng(42); base=X[:4000]; rotations=rng.integers(0,4,len(base)); x_ssl=np.asarray([np.rot90(img,k).copy() for img,k in zip(base,rotations)])
    ssl_model=tf.keras.Sequential([tf.keras.layers.Input(shape=(28,28,1)),tf.keras.layers.Conv2D(32,3,activation="relu"),tf.keras.layers.MaxPooling2D(2),tf.keras.layers.Conv2D(64,3,activation="relu"),tf.keras.layers.MaxPooling2D(2),tf.keras.layers.Flatten(),tf.keras.layers.Dense(128,activation="relu",name="encoder"),tf.keras.layers.Dense(4,activation="softmax")])
    ssl_model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"]); history=ssl_model.fit(x_ssl,rotations,epochs=3,batch_size=128,validation_split=.1,verbose=0)
    encoder=tf.keras.Model(ssl_model.inputs,ssl_model.get_layer("encoder").output); train_idx=np.arange(0,8000,10); train_features=encoder.predict(X[train_idx],verbose=0); test_features=encoder.predict(X[8000:],verbose=0)
    model=LogisticRegression(max_iter=600).fit(train_features,y[train_idx]); pred=model.predict(test_features)
    return {"project":25,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"MNIST","records":len(X),"labeled_training_images":len(train_idx),"model":"rotation-prediction CNN with transferred encoder","metrics":{"accuracy":round(float(accuracy_score(y[8000:],pred)),4),"rotation_accuracy":round(float(history.history['val_accuracy'][-1]),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
