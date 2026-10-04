import wave
from pathlib import Path
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.metrics import accuracy_score
from download_data import ensure_dataset
PROJECT_TITLE="Gaussian Mixture Models for Speaker Identification"
def features(path):
    with wave.open(str(path),"rb") as w: raw=w.readframes(w.getnframes()); width=w.getsampwidth(); channels=w.getnchannels()
    dtype=np.int16 if width==2 else np.int8; signal=np.frombuffer(raw,dtype=dtype).astype(float)
    if channels>1: signal=signal.reshape(-1,channels).mean(axis=1)
    signal=signal/(np.max(np.abs(signal))+1e-9); chunks=np.array_split(signal,20); rows=[]
    for x in chunks:
        spec=np.abs(np.fft.rfft(x*np.hanning(len(x)))); bands=np.array_split(spec,12); rows.append([np.log1p(b.mean()) for b in bands]+[np.sqrt(np.mean(x*x)),np.mean(np.abs(np.diff(np.signbit(x))))])
    return np.asarray(rows)
def run_demo():
    root=ensure_dataset().parent; files=sorted(root.glob("Actor_*/*.wav")); train={}; test=[]
    for i,path in enumerate(files):
        speaker=path.parent.name
        if i%5==0: test.append((speaker,path))
        else: train.setdefault(speaker,[]).append(path)
    models={speaker:GaussianMixture(n_components=4,covariance_type="diag",random_state=42).fit(np.vstack([features(p) for p in paths])) for speaker,paths in train.items()}
    truth=[]; predicted=[]
    for speaker,path in test:
        feat=features(path); truth.append(speaker); predicted.append(max(models,key=lambda s:models[s].score(feat)))
    return {"project":28,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"RAVDESS speech audio","records":len(files),"speakers":len(models),"metrics":{"accuracy":round(float(accuracy_score(truth,predicted)),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
