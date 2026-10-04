"""Extract contact details, skills, education, and experience from a resume."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import load_resume_text, parse_resume

PROJECT_NUMBER = 35
PROJECT_TITLE = "Resume Parser"
AUTHOR = "Edward Ocran"


class _Entity:
    def __init__(self, text, label):
        self.text, self.label_ = text, label


class _Document:
    ents = [_Entity("Jordan Mensah", "PERSON")]


def _validation_nlp(text):
    return _Document()


def run_demo(fast: bool | None = None, path: Path | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    source = path or HERE / "data" / "sample_resume.txt"
    parsed = parse_resume(load_resume_text(source), nlp=_validation_nlp if fast else None)
    populated = sum(bool(parsed[key]) for key in ("name", "email", "phone", "skills", "education", "experience"))
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "input": source.name, "result": parsed, "metrics": {"fields_extracted": populated, "skills_found": len(parsed["skills"])}}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("resume", nargs="?", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo(path=args.resume)
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
