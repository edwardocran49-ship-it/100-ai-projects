"""Generate, execute, diagnose, and repair a Python function."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT))
from portfolio_core.agents import coding_bot
PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 52, "Coding Bot with Tool Use", "Edward Ocran"


def run_demo():
    result = coding_bot("Write a Python function that checks if a number is prime.")
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "task": result["task"], "final_code": result["code"], "attempts": result["attempts"],
            "metrics": {"attempt_count": len(result["attempts"]), "tests_passed": result["tests_passed"], "tests_total": result["tests_total"]}}


def main():
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); result=run_demo()
    print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__ == "__main__": main()
