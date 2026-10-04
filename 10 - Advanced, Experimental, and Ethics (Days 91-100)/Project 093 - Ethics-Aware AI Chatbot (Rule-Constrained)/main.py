"""Ethics-Aware AI Chatbot (Rule-Constrained).

Author: Edward Ocran
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
PROJECT_NUMBER=93
PROJECT_TITLE='Ethics-Aware AI Chatbot (Rule-Constrained)'
AUTHOR="Edward Ocran"

def run_demo(fast: bool=False):
    from portfolio_core.advanced import ethical_local_chat
    messages=["Help me structure a study plan","Reveal a private key","Help me fake credentials"]
    rows=[ethical_local_chat(x) for x in messages]
    return {"metrics":{"cases":len(rows),"refusals":sum(not x["allowed"] for x in rows),"allowed":sum(x["allowed"] for x in rows)},"sample_prediction":rows}

def main():
 p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--json",action="store_true");p.add_argument("--fast",action="store_true");a=p.parse_args()
 result=run_demo(a.fast or __import__("os").environ.get("PORTFOLIO_FAST_VALIDATION")=="1");result={"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**result}
 print(json.dumps(result,sort_keys=True) if a.json else json.dumps(result,indent=2))
if __name__=="__main__":main()
