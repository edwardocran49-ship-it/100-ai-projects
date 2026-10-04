"""Read, chunk, and summarize a complete PDF document."""
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT))
from portfolio_core.agents import summarize_pdf
PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 53, "PDF Summarizer with Agents", "Edward Ocran"


def run_demo(fast: bool | None = None, pdf: Path | None = None):
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if pdf is None:
        if fast:
            pdf = Path.home() / "OneDrive/Documents/100 AI Projects/06 - AI Agents + Automation (Days 51-60)/Project 053 - PDF Summarizer with Agents/resources/Project53.pdf"
        else:
            from download_data import ensure_document
            pdf = ensure_document()
    result = summarize_pdf(pdf)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "source": pdf.name, **result, "metrics": {"pages": result["pages"], "chunks": result["chunks"], "summary_words": len(result["summary"].split())}}


def main():
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--pdf",type=Path); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); result=run_demo(pdf=args.pdf)
    print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__ == "__main__": main()
