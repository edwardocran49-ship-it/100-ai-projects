"""BCI Signal Classifier (OpenBCI Data).

Author: Edward Ocran
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
PROJECT_NUMBER=96
PROJECT_TITLE='BCI Signal Classifier (OpenBCI Data)'
AUTHOR="Edward Ocran"

def run_demo(fast: bool=False):
    from portfolio_core.advanced import classify_bci,parse_openbci
    data=Path(__file__).parent/"data"
    if not fast and (data/"meditation.txt").exists():
     recordings=[("active",parse_openbci(data/"blinks-jawclench-alpha.txt")),("meditation",parse_openbci(data/"meditation.txt"))]
     r=classify_bci(recordings)
    else:
     rng=np.random.default_rng(96);t=np.arange(250*24)/250
     active=np.column_stack([np.sin(2*np.pi*22*t)+.25*rng.normal(size=t.size) for _ in range(8)])
     calm=np.column_stack([1.5*np.sin(2*np.pi*10*t)+.25*rng.normal(size=t.size) for _ in range(8)])
     r=classify_bci([("active",active),("meditation",calm)])
    return {"metrics":{"accuracy":r["accuracy"],"windows":r["windows"],**r["feature_importance"]},"sample_prediction":r["confusion_matrix"]}

def main():
 p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--json",action="store_true");p.add_argument("--fast",action="store_true");a=p.parse_args()
 result=run_demo(a.fast or __import__("os").environ.get("PORTFOLIO_FAST_VALIDATION")=="1");result={"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**result}
 print(json.dumps(result,sort_keys=True) if a.json else json.dumps(result,indent=2))
if __name__=="__main__":main()
