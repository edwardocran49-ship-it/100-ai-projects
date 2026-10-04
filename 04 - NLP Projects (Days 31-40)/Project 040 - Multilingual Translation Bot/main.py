"""Translate English text into French with a Marian transformer."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import token_overlap, translate_text

PROJECT_NUMBER = 40
PROJECT_TITLE = "Multilingual Translation Bot"
AUTHOR = "Edward Ocran"
SOURCE = "Reliable data helps teams make better decisions."
REFERENCE = "Des données fiables aident les équipes à prendre de meilleures décisions."


def _validation_backend(text):
    return [{"translation_text": REFERENCE}]


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    translation = translate_text(SOURCE, backend=_validation_backend if fast else None)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "Helsinki-NLP/opus-mt-en-fr", "source_language": "English", "target_language": "French",
            "source": SOURCE, "translation": translation,
            "metrics": {"reference_token_overlap": round(token_overlap(REFERENCE, translation), 3),
                        "source_words": len(SOURCE.split()), "translated_words": len(translation.split())}}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True) if args.json else json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
