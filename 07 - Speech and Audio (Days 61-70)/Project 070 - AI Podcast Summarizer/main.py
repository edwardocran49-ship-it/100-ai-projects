"""Transcribe long-form audio, chunk the transcript, and prepare episode notes."""
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.agents import chunk_text,summarize_text
from portfolio_core.speech import transcribe_vosk
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=70,"AI Podcast Summarizer","Edward Ocran"
DEMO=("Data teams often begin with a dashboard, but the more durable work starts with a decision. "
"A useful metric has a clear owner, a stable definition, and a threshold that changes an action. "
"Analysts should inspect missing values and duplicates before interpreting movement. "
"They should also separate an observed association from a causal claim. "
"The episode closes by recommending short written decision logs so later reviewers can see what evidence was available.")
def run_demo(fast:bool|None=None,audio:Path|None=None,model:Path|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast;transcript=DEMO if fast else transcribe_vosk(audio,model or ROOT/".models"/"vosk-model-small-en-us-0.15")
    chunks=chunk_text(transcript,180);summaries=[summarize_text(c,2) for c in chunks];summary=" ".join(summaries)
    notes=[part.strip() for part in summary.split(". ") if part.strip()]
    return {"project":70,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","summary":summary,"episode_notes":notes,"metrics":{"transcript_words":len(transcript.split()),"chunks":len(chunks),"summary_words":len(summary.split()),"compression":round(len(summary.split())/len(transcript.split()),3)}}
def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--audio",type=Path);p.add_argument("--model",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(audio=a.audio,model=a.model);print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
