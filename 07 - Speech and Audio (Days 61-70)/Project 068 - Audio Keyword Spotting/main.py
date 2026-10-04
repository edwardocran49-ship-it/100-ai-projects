"""Train a compact keyword spotter on Google Speech Commands."""
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.audio import classify_dataset,write_tone
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=68,"Audio Keyword Spotting","Edward Ocran"
WORDS=("yes","no","up","down","left","right","on","off","stop","go")
def load_commands(root:Path,limit=100):
    files=[];labels=[]
    for word in WORDS:
        choices=sorted((root/word).glob("*.wav"))[:limit];files.extend(choices);labels.extend([word]*len(choices))
    return files,labels
def run_demo(fast:bool|None=None,data:Path|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast
    if fast:
        d=Path(__file__).parent/".validation_audio";d.mkdir(exist_ok=True);files=[];labels=[]
        for label,freq in (("yes",240),("stop",760)):
            for i in range(8):files.append(write_tone(d/f"{label}{i}.wav",freq+i*3));labels.append(label)
    else:
        data=data or Path(__file__).parent/"data"
        if not data.exists(): raise FileNotFoundError("Run download_data.py first or provide --data with extracted Speech Commands")
        files,labels=load_commands(data)
        if not files: raise ValueError(f"No Speech Commands WAV files found under {data}")
    result=classify_dataset(files,labels,68)
    return {"project":68,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","dataset":"Google Speech Commands v0.01","metrics":{k:v for k,v in result.items() if k not in {"model","truth","predictions","confusion_matrix"}},"confusion_matrix":result["confusion_matrix"]}
def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--data",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(data=a.data);print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
