"""Simulated Society of AI Agents (LangGraph).

Author: Edward Ocran
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
PROJECT_NUMBER=97
PROJECT_TITLE='Simulated Society of AI Agents (LangGraph)'
AUTHOR="Edward Ocran"

def run_demo(fast: bool=False):
    from portfolio_core.advanced import simulate_society,simulate_society_langgraph
    r=simulate_society(12) if fast else simulate_society_langgraph(12)
    return {"metrics":{"messages":len(r["messages"]),"roles":len(r["participation"]),**r["participation"]},"sample_prediction":{"winning_priority":r["winning_priority"],"agenda":r["agenda"]}}

def main():
 p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--json",action="store_true");p.add_argument("--fast",action="store_true");a=p.parse_args()
 result=run_demo(a.fast or __import__("os").environ.get("PORTFOLIO_FAST_VALIDATION")=="1");result={"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**result}
 print(json.dumps(result,sort_keys=True) if a.json else json.dumps(result,indent=2))
if __name__=="__main__":main()
