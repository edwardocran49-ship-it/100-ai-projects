"""Classify files and move them into category folders."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from portfolio_core.agents import organize_folder
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=56,"File Organizer Agent (Desktop AI)","Edward Ocran"


def run_demo(folder:Path|None=None):
    if folder is None:
        folder=Path(__file__).resolve().parent / "fixtures"; move=False
    else:
        move=True
    result=organize_folder(folder,move=move)
    return {"project":PROJECT_NUMBER,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","mode":"move" if move else "preview",
            "metrics":{"files_processed":result["files"],"categories_created":len(result["categories"])},**result}


def main():
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--folder",type=Path); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); result=run_demo(args.folder); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
