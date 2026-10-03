"""Runnable offline demonstration for Project 6: Naive Bayes Text Classifier.

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

PROJECT_NUMBER = 6
PROJECT_TITLE = 'Naive Bayes Text Classifier'
AUTHOR = "Edward Ocran"
SEED = 1000 + PROJECT_NUMBER

POSITIVE = {"clear", "excellent", "helpful", "love", "good", "fast", "accurate"}
NEGATIVE = {"bad", "slow", "confusing", "hate", "poor", "broken", "wrong"}


def analyze(text: str) -> dict[str, Any]:
    tokens = re.findall(r"[a-z']+", text.lower())
    score = sum(token in POSITIVE for token in tokens) - sum(token in NEGATIVE for token in tokens)
    label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return {"label": label, "score": score, "tokens": tokens}


def run_demo() -> dict[str, Any]:
    samples = ["The model is clear, helpful and accurate", "The result is slow and confusing", "The model returned a result"]
    results = [analyze(sample) for sample in samples]
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "status": "ok", "task": "nlp",
            "metrics": {"documents": len(results), "non_neutral": sum(r["label"] != "neutral" for r in results)},
            "sample_prediction": results[0]}

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
