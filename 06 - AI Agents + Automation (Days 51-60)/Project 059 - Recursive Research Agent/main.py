"""Decompose a research question, retrieve evidence, and synthesize a report."""
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from portfolio_core.agents import recursive_research
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=59,"Recursive Research Agent","Edward Ocran"


def source_text(fast:bool)->str:
    if fast: return "Cryptocurrency mining consumes electricity. Its emissions depend on the generation mix. Renewable energy, efficient hardware, and less energy-intensive consensus mechanisms can reduce impacts."
    import requests
    from bs4 import BeautifulSoup
    url="https://en.wikipedia.org/wiki/Environmental_impact_of_bitcoin"
    response=requests.get(url,timeout=30,headers={"User-Agent":"portfolio-research/1.0"}); response.raise_for_status()
    soup=BeautifulSoup(response.text,"html.parser")
    return "\n".join(paragraph.get_text(" ",strip=True) for paragraph in soup.find_all("p") if paragraph.get_text(strip=True))


def run_demo(fast:bool|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast
    result=recursive_research("What are the environmental impacts of cryptocurrency mining?",source_text(fast))
    return {"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok",**result,
            "metrics":{"subquestions":len(result["subquestions"]),"answered":len(result["answers"]),"chunks_indexed":result["chunks_indexed"]}}


def main():
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
