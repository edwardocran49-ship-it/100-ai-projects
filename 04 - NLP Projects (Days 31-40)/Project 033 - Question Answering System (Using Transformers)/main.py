"""Extractive question answering with a SQuAD-trained transformer."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import answer_question

PROJECT_NUMBER = 33
PROJECT_TITLE = "Question Answering System (Using Transformers)"
AUTHOR = "Edward Ocran"
CONTEXT = "The James Webb Space Telescope was launched on 25 December 2021 from French Guiana. It observes primarily in infrared wavelengths."
QUESTION = "When was the James Webb Space Telescope launched?"


def _validation_backend(**kwargs):
    answer = "25 December 2021"
    start = kwargs["context"].index(answer)
    return {"answer": answer, "score": 0.98, "start": start, "end": start + len(answer)}


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    result = answer_question(QUESTION, CONTEXT, backend=_validation_backend if fast else None)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "distilbert-base-cased-distilled-squad", "question": QUESTION, "result": result,
            "metrics": {"answer_confidence": result["score"], "context_characters": len(CONTEXT)}}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
