"""Classify text into user-supplied labels without task-specific training."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import zero_shot_classify

PROJECT_NUMBER = 38
PROJECT_TITLE = "Zero-Shot Text Classification"
AUTHOR = "Edward Ocran"
TEXT = "The central bank held interest rates steady after inflation eased."
LABELS = ["economy", "technology", "sports", "health"]


def _validation_backend(text, candidate_labels, multi_label=False):
    return {"labels": ["economy", "technology", "health", "sports"], "scores": [0.91, 0.04, 0.03, 0.02]}


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    rankings = zero_shot_classify(TEXT, LABELS, backend=_validation_backend if fast else None)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "facebook/bart-large-mnli", "text": TEXT, "rankings": rankings,
            "metrics": {"labels_considered": len(LABELS), "top_confidence": rankings[0]["score"]}}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
