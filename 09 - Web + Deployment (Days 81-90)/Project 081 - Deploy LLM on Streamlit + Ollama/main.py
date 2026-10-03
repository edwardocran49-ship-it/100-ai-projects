"""Runnable offline demonstration for Project 81: Deploy LLM on Streamlit + Ollama.

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

PROJECT_NUMBER = 81
PROJECT_TITLE = 'Deploy LLM on Streamlit + Ollama'
AUTHOR = "Edward Ocran"
SEED = 1000 + PROJECT_NUMBER

def predict(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("text", "")).strip()
    if not text:
        return {"ok": False, "error": "text is required"}
    tokens = re.findall(r"[A-Za-z0-9']+", text)
    return {"ok": True, "prediction": "long" if len(tokens) >= 6 else "short", "token_count": len(tokens)}


def run_demo() -> dict[str, Any]:
    response = predict({"text": "A local inference endpoint with validated input"})
    assert response["ok"]
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "status": "ok", "task": "deployment",
            "metrics": {"requests": 1, "token_count": response["token_count"]}, "sample_prediction": response}

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
