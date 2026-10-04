"""Build a Local AGI Agent with Memory + Tools.

Author: Edward Ocran
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
PROJECT_NUMBER=91
PROJECT_TITLE='Build a Local AGI Agent with Memory + Tools'
AUTHOR="Edward Ocran"

def run_demo(fast: bool=False):
    from portfolio_core.advanced import LocalAgent
    memory_file=Path(__file__).with_name(".agent_memory.json")
    if memory_file.exists(): memory_file.unlink()
    agent=LocalAgent(memory_file);agent.remember("Edward prefers transparent, locally executed tools.")
    results=[agent.act("calculate 12 * (3 + 2)"),agent.act("What does Edward prefer?")]
    memory_file.unlink(missing_ok=True)
    return {"metrics":{"tool_calls":len(results),"memory_items":len(agent.memory),"calculator_answer":results[0]["answer"]},"sample_prediction":results}

def main():
 p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--json",action="store_true");p.add_argument("--fast",action="store_true");a=p.parse_args()
 result=run_demo(a.fast or __import__("os").environ.get("PORTFOLIO_FAST_VALIDATION")=="1");result={"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**result}
 print(json.dumps(result,sort_keys=True) if a.json else json.dumps(result,indent=2))
if __name__=="__main__":main()
