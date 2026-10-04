"""Train a voice-emotion classifier on the RAVDESS speech dataset."""
from __future__ import annotations
import argparse,json,os,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.audio import classify_dataset,write_tone
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=67,"Voice Emotion Classifier","Edward Ocran"
MAP={"01":"neutral","02":"calm","03":"happy","04":"sad","05":"angry","06":"fearful","07":"disgust","08":"surprised"}
def load_ravdess(root:Path,limit=24):
    selected=[];counts=Counter()
    for path in sorted(root.rglob("*.wav")):
        parts=path.stem.split("-");label=MAP.get(parts[2]) if len(parts)>=3 else None
        if label and counts[label]<limit: selected.append(path);counts[label]+=1
    return selected,[MAP[p.stem.split("-")[2]] for p in selected]
def run_demo(fast:bool|None=None,data:Path|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast
    if fast:
        d=Path(__file__).parent/".validation_audio";d.mkdir(exist_ok=True);files=[];labels=[]
        for label,freq in (("calm",180),("angry",680)):
            for i in range(8):files.append(write_tone(d/f"{label}{i}.wav",freq+i*4));labels.append(label)
    else:
        data=data or Path(__file__).parent/"data"
        if not data.exists(): raise FileNotFoundError("Run download_data.py first or provide --data with the RAVDESS directory")
        files,labels=load_ravdess(data)
        if not files: raise ValueError(f"No RAVDESS WAV files found under {data}")
    result=classify_dataset(files,labels,67)
    return {"project":67,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","dataset":"RAVDESS","metrics":{k:v for k,v in result.items() if k not in {"model","truth","predictions","confusion_matrix"}},"confusion_matrix":result["confusion_matrix"]}
def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--data",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(data=a.data);print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
