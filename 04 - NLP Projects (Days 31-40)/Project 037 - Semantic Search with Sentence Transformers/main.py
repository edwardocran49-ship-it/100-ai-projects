"""Rank a document collection using sentence-transformer embeddings."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.nlp import semantic_search

PROJECT_NUMBER = 37
PROJECT_TITLE = "Semantic Search with Sentence Transformers"
AUTHOR = "Edward Ocran"
DOCUMENTS = [
    "Solar panels convert sunlight into electricity for homes and businesses.",
    "Wind turbines generate power from moving air.",
    "Battery storage balances renewable electricity supply and demand.",
    "A balanced portfolio can reduce exposure to market volatility.",
    "Sleep quality affects concentration and long-term health.",
]
QUERY = "How can excess renewable power be saved for later?"


def _validation_encoder(values):
    mapping = {
        DOCUMENTS[0]: [0.7, 0.3, 0.0], DOCUMENTS[1]: [0.6, 0.4, 0.0],
        DOCUMENTS[2]: [1.0, 0.0, 0.0], DOCUMENTS[3]: [0.0, 0.2, 0.8],
        DOCUMENTS[4]: [0.0, 0.0, 1.0], QUERY: [0.95, 0.05, 0.0],
    }
    return np.asarray([mapping[value] for value in values])


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    results = semantic_search(QUERY, DOCUMENTS, encoder=_validation_encoder if fast else None, top_k=3)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "sentence-transformers/all-MiniLM-L6-v2", "query": QUERY, "results": results,
            "metrics": {"documents_searched": len(DOCUMENTS), "top_score": results[0]["score"]}}


def main() -> None:
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
