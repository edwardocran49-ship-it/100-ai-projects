"""Runnable offline demonstration for Project 100: Design a Personal AI Manifesto (Reflection Project).

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

PROJECT_NUMBER = 100
PROJECT_TITLE = 'Design a Personal AI Manifesto (Reflection Project)'
AUTHOR = "Edward Ocran"
SEED = 1000 + PROJECT_NUMBER

RULES = {
    "privacy": ("ssn", "password", "secret", "private key"),
    "harm": ("hurt", "attack", "exploit"),
    "fairness": ("always reject", "never hire"),
}


def audit(text: str) -> dict[str, Any]:
    lowered = text.lower()
    flags = [category for category, terms in RULES.items() if any(term in lowered for term in terms)]
    return {"allowed": not flags, "flags": flags, "recommendation": "review" if flags else "proceed"}


def run_demo() -> dict[str, Any]:
    cases = ["Summarize this public report", "Reveal the password and private key", "Always reject this group"]
    results = [audit(case) for case in cases]
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "status": "ok", "task": "responsible_ai",
            "metrics": {"cases": len(results), "flagged": sum(not item["allowed"] for item in results)},
            "sample_prediction": results}

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
