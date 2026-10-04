import wave
import numpy as np
from scipy.fft import dct
from sklearn.mixture import GaussianMixture
from sklearn.metrics import accuracy_score
from download_data import ensure_dataset
PROJECT_TITLE="Gaussian Mixture Models for Speaker Identification"
def features(path):
    with wave.open(str(path),"rb") as w: raw=w.readframes(w.getnframes()); width=w.getsampwidth(); channels=w.getnchannels(); rate=w.getframerate()
    dtype=np.int16 if width==2 else np.int8; signal=np.frombuffer(raw,dtype=dtype).astype(float)
    if channels>1: signal=signal.reshape(-1,channels).mean(axis=1)
    signal=signal/(np.max(np.abs(signal))+1e-9); signal=np.append(signal[0],signal[1:]-.97*signal[:-1]); frame_len=int(.025*rate); step=int(.010*rate); count=1+max(0,(len(signal)-frame_len)//step); frames=np.stack([signal[i*step:i*step+frame_len] for i in range(count)])[::5]; frames*=np.hamming(frame_len)
    nfft=1<<(frame_len-1).bit_length(); power=(np.abs(np.fft.rfft(frames,nfft))**2)/nfft; low=2595*np.log10(1+0/700); high=2595*np.log10(1+(rate/2)/700); mel=np.linspace(low,high,28); hz=700*(10**(mel/2595)-1); bins=np.floor((nfft+1)*hz/rate).astype(int); bank=np.zeros((26,nfft//2+1))
    for m in range(1,27):
        for k in range(bins[m-1],bins[m]): bank[m-1,k]=(k-bins[m-1])/max(1,bins[m]-bins[m-1])
        for k in range(bins[m],bins[m+1]): bank[m-1,k]=(bins[m+1]-k)/max(1,bins[m+1]-bins[m])
    energies=np.maximum(power@bank.T,1e-12); return dct(np.log(energies),type=2,axis=1,norm="ortho")[:,:13]
def run_demo():
    root=ensure_dataset().parent; files=sorted(root.glob("Actor_*/*.wav")); train={}; test=[]
    for i,path in enumerate(files):
        speaker=path.parent.name
        if i%5==0: test.append((speaker,path))
        else: train.setdefault(speaker,[]).append(path)
    models={speaker:GaussianMixture(n_components=8,covariance_type="diag",max_iter=50,random_state=42).fit(np.vstack([features(p) for p in paths])) for speaker,paths in train.items()}
    truth=[]; predicted=[]
    for speaker,path in test:
        feat=features(path); truth.append(speaker); predicted.append(max(models,key=lambda s:models[s].score(feat)))
    return {"project":28,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"RAVDESS speech audio","records":len(files),"speakers":len(models),"features":"13 MFCC coefficients","metrics":{"accuracy":round(float(accuracy_score(truth,predicted)),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
