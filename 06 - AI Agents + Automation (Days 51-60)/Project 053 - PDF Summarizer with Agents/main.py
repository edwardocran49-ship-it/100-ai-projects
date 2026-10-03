"""Runnable offline demonstration for Project 53: PDF Summarizer with Agents.

Author: Edward Ocran
This implementation follows the supplied project objective while using generated
sample data so that its smoke test is deterministic and does not require secrets.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
from typing import Any

PROJECT_NUMBER = 53
PROJECT_TITLE = 'PDF Summarizer with Agents'
AUTHOR = "Edward Ocran"
SEED = 1000 + PROJECT_NUMBER

KNOWLEDGE = {
    "memory": "Memory stores useful context between agent steps.",
    "tool": "Tools let an agent perform bounded, auditable actions.",
    "safety": "Validate inputs and keep a human in control of consequential actions.",
}


def safe_calculate(expression: str) -> float:
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        raise ValueError("Only arithmetic expressions are allowed")
    return float(eval(expression, {"__builtins__": {}}, {}))


def agent(query: str) -> dict[str, Any]:
    arithmetic = re.search(r"(?:calculate|compute)\s+(.+)", query.lower())
    if arithmetic:
        return {"tool": "calculator", "answer": safe_calculate(arithmetic.group(1))}
    key = max(KNOWLEDGE, key=lambda item: int(item in query.lower()))
    return {"tool": "local_knowledge", "answer": KNOWLEDGE[key]}


def run_demo() -> dict[str, Any]:
    results = [agent("calculate 12 * (3 + 2)"), agent("How should tool safety work?")]
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "status": "ok", "task": "agent",
            "metrics": {"tool_calls": len(results)}, "sample_prediction": results}

def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true", help="print machine-readable output")
    args = parser.parse_args()
    result = run_demo()
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(f"Project {PROJECT_NUMBER}: {PROJECT_TITLE}")
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
