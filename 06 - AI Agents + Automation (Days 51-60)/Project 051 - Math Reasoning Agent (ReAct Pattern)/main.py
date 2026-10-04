"""Solve word problems with an explicit reason-act-observe-answer trace."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT))
from portfolio_core.agents import math_agent
PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 51, "Math Reasoning Agent (ReAct Pattern)", "Edward Ocran"


def run_demo():
    questions = ["A rectangle has length 8 and width 5. What is its area?",
                 "What is the square of the sum of 3 and 4?",
                 "What is 12 divided by 3 and then multiplied by 4?"]
    traces = [math_agent(question) for question in questions]
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "pattern": "ReAct", "traces": traces,
            "metrics": {"problems": len(traces), "correct": sum(item["final_answer"] == expected for item, expected in zip(traces, (40, 49, 16))),
                        "calculator_calls": sum(item["tool_calls"] for item in traces)}}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true"); args = parser.parse_args()
    result = run_demo(); print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))
if __name__ == "__main__": main()
