"""Read a webpage once, store chunks, and retrieve relevant passages."""
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from portfolio_core.agents import VectorMemory,summarize_text
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=57,"Browser Agent with Memory","Edward Ocran"


def fetch_page(url:str)->str:
    import requests
    from bs4 import BeautifulSoup
    response=requests.get(url,timeout=30,headers={"User-Agent":"portfolio-research/1.0"}); response.raise_for_status()
    soup=BeautifulSoup(response.text,"html.parser")
    return "\n".join(paragraph.get_text(" ",strip=True) for paragraph in soup.find_all("p") if paragraph.get_text(strip=True))


def run_demo(fast:bool|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast
    url="https://en.wikipedia.org/wiki/Artificial_intelligence"
    text=("Artificial intelligence became an academic discipline in 1956. The field went through cycles of optimism and funding, followed by periods called AI winters. Machine learning later became central to progress." if fast else fetch_page(url))
    memory=VectorMemory(); chunks=memory.memorize(text,url,800); passages=memory.query("history Dartmouth 1956 Turing AI winter expert systems machine learning",3)
    answer=" ".join(summarize_text(item["text"],1) for item in passages if item["score"]>0)
    return {"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","source":url,"answer":answer,"passages":passages,
            "metrics":{"chunks_stored":chunks,"retrieved":len(passages),"best_similarity":passages[0]["score"]}}


def main():
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
