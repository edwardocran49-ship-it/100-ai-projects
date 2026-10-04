"""Abstractive text summarization with T5."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import summarize_text

PROJECT_NUMBER = 32
PROJECT_TITLE = "Text Summarizer with T5"
AUTHOR = "Edward Ocran"
ARTICLE = ("Coastal cities are expanding flood defenses as rainfall becomes less predictable. "
           "Engineers are combining restored wetlands with barriers and improved drainage. "
           "The mixed approach lowers surge risk while preserving habitats and public access. "
           "Local monitoring will determine which interventions receive additional funding.")


def _validation_backend(text, **kwargs):
    return [{"summary_text": "Cities are combining natural and engineered flood defenses."}]


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    summary = summarize_text(ARTICLE, backend=_validation_backend if fast else None)
    source_words, summary_words = len(ARTICLE.split()), len(summary.split())
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "google-t5/t5-small", "metrics": {"source_words": source_words,
            "summary_words": summary_words, "compression_ratio": round(summary_words / source_words, 3)},
            "summary": summary}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
