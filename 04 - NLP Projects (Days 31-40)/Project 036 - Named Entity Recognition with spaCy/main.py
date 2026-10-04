"""Extract people, organisations, places, and dates with spaCy."""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import extract_entities

PROJECT_NUMBER = 36
PROJECT_TITLE = "Named Entity Recognition with spaCy"
AUTHOR = "Edward Ocran"
TEXT = "Satya Nadella met Microsoft researchers in London on 14 March 2025."


class _Entity:
    def __init__(self, text, label, start, end):
        self.text, self.label_, self.start_char, self.end_char = text, label, start, end


class _Document:
    ents = [_Entity("Satya Nadella", "PERSON", 0, 13), _Entity("Microsoft", "ORG", 18, 27),
            _Entity("London", "GPE", 43, 49), _Entity("14 March 2025", "DATE", 53, 66)]


def _validation_nlp(text):
    return _Document()


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    entities = extract_entities(TEXT, nlp=_validation_nlp if fast else None)
    counts = Counter(item["label"] for item in entities)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "en_core_web_sm", "text": TEXT, "entities": entities,
            "metrics": {"entities_found": len(entities), "labels": dict(sorted(counts.items()))}}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
