"""Model Cards + Datasheets Generator.

Author: Edward Ocran
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
PROJECT_NUMBER=95
PROJECT_TITLE='Model Cards + Datasheets Generator'
AUTHOR="Edward Ocran"

def run_demo(fast: bool=False):
    from portfolio_core.advanced import write_governance_docs
    model={"name":"Risk Triage Classifier","owner":"Edward Ocran","version":"1.0","intended_use":"Prioritize records for qualified human review; never make an adverse decision automatically.","metric":"held-out F1","score":.842,"evaluation_population":"stratified validation records","limitations":"Performance may shift across institutions and rare subgroups. Human review is mandatory.","monitoring":"Track drift, subgroup recall, overrides, and complaints each month."}
    data={"name":"Triage Benchmark","purpose":"Support reproducible evaluation of triage ranking.","rows":12500,"features":18,"collection":"Records were collected under documented consent and access controls.","preprocessing":"Identifiers were removed and transformations were versioned.","uses":"Use for evaluation and controlled research; do not re-identify individuals.","maintenance":"The owner reviews provenance, access, and retention quarterly."}
    paths=write_governance_docs(Path(__file__).parent,model,data)
    return {"metrics":{"documents":len(paths),"required_sections":8,"model_score":model["score"]},"sample_prediction":paths}

def main():
 p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--json",action="store_true");p.add_argument("--fast",action="store_true");a=p.parse_args()
 result=run_demo(a.fast or __import__("os").environ.get("PORTFOLIO_FAST_VALIDATION")=="1");result={"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**result}
 print(json.dumps(result,sort_keys=True) if a.json else json.dumps(result,indent=2))
if __name__=="__main__":main()
