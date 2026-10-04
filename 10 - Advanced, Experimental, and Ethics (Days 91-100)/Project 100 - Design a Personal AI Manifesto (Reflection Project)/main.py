"""Design a Personal AI Manifesto (Reflection Project).

Author: Edward Ocran
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
PROJECT_NUMBER=100
PROJECT_TITLE='Design a Personal AI Manifesto (Reflection Project)'
AUTHOR="Edward Ocran"

def run_demo(fast: bool=False):
    path=Path(__file__).with_name("PERSONAL_AI_MANIFESTO.md")
    text=path.read_text(encoding="utf-8") if path.exists() else "## Philosophy\n## Should be\n## Always\n## Never\n## Future\n"+"\n".join(f"{i}. Commitment" for i in range(1,10))
    sections=[line for line in text.splitlines() if line.startswith("## ")]
    commitments=[line for line in text.splitlines() if line.lstrip().startswith(tuple(f"{i}." for i in range(1,10)))]
    return {"metrics":{"sections":len(sections),"commitments":len(commitments),"words":len(text.split())},"sample_prediction":sections}

def main():
 p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--json",action="store_true");p.add_argument("--fast",action="store_true");a=p.parse_args()
 result=run_demo(a.fast or __import__("os").environ.get("PORTFOLIO_FAST_VALIDATION")=="1");result={"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**result}
 print(json.dumps(result,sort_keys=True) if a.json else json.dumps(result,indent=2))
if __name__=="__main__":main()
