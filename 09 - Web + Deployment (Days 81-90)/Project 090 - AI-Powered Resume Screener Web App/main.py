"""Runnable core for Project 90: AI-Powered Resume Screener Web App."""
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.deployment import run_project
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=90,'AI-Powered Resume Screener Web App',"Edward Ocran"
def run_demo(fast=None):return {"title":PROJECT_TITLE,**run_project(PROJECT_NUMBER,Path(__file__).parent,True if fast is None else fast)}
def main():
 p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--json",action="store_true");a=p.parse_args();print(json.dumps(run_demo(),indent=None if a.json else 2))
if __name__=="__main__":main()
