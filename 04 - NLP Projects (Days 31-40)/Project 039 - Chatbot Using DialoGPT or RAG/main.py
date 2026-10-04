"""A conversational response demo backed by DialoGPT-small."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import dialog_reply

PROJECT_NUMBER = 39
PROJECT_TITLE = "Chatbot Using DialoGPT or RAG"
AUTHOR = "Edward Ocran"
MESSAGE = "What makes a productive morning routine?"


def _validation_backend(message, history):
    return "Start with one consistent task, protect a short focus block, and review what worked."


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    history = [("Hello", "Hi. What would you like to discuss?")]
    response = dialog_reply(MESSAGE, history=history, backend=_validation_backend if fast else None)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "microsoft/DialoGPT-small", "message": MESSAGE, "response": response,
            "metrics": {"history_turns": len(history), "response_words": len(response.split())}}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
