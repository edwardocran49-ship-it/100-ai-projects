"""Train an environmental-sound classifier on a real UrbanSound8K subset."""
from __future__ import annotations
import argparse,csv,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.audio import classify_dataset,write_tone
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=64,"Sound Classification (UrbanSound8K)","Edward Ocran"

def load_manifest(data:Path):
    rows=list(csv.DictReader((data/"manifest.csv").open(encoding="utf-8")))
    return [data/r["file"] for r in rows],[r["label"] for r in rows]
def run_demo(fast:bool|None=None,data:Path|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast;data=data or Path(__file__).parent/"data"
    if fast:
        d=Path(__file__).parent/".validation_audio";d.mkdir(exist_ok=True);files=[];labels=[]
        for label,freq in (("dog_bark",180),("siren",920)):
            for i in range(8): files.append(write_tone(d/f"{label}{i}.wav",freq+i*3));labels.append(label)
    else:
        if not (data/"manifest.csv").exists(): raise FileNotFoundError("Run download_data.py first")
        files,labels=load_manifest(data)
    result=classify_dataset(files,labels,64)
    return {"project":64,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","dataset":"UrbanSound8K","metrics":{k:v for k,v in result.items() if k not in {"model","truth","predictions","confusion_matrix"}},"confusion_matrix":result["confusion_matrix"]}
def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--data",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(data=a.data);print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
