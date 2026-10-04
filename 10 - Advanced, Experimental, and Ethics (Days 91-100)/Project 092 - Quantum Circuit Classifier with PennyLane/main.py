"""Quantum Circuit Classifier with PennyLane.

Author: Edward Ocran
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
PROJECT_NUMBER=92
PROJECT_TITLE='Quantum Circuit Classifier with PennyLane'
AUTHOR="Edward Ocran"

def run_demo(fast: bool=False):
    from portfolio_core.advanced import pennylane_xor,quantum_xor
    r=quantum_xor(40) if fast else pennylane_xor(100)
    return {"metrics":{"accuracy":r["accuracy"],"final_loss":r["loss"],"states":4},"sample_prediction":r["predictions"]}

def main():
 p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--json",action="store_true");p.add_argument("--fast",action="store_true");a=p.parse_args()
 result=run_demo(a.fast or __import__("os").environ.get("PORTFOLIO_FAST_VALIDATION")=="1");result={"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**result}
 print(json.dumps(result,sort_keys=True) if a.json else json.dumps(result,indent=2))
if __name__=="__main__":main()
