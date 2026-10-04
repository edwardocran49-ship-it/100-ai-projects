"""Transcribe a spoken question, retrieve evidence, and answer from context."""
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.agents import VectorMemory,summarize_text
from portfolio_core.speech import transcribe_vosk
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=69,"Whisper + RAG Agent","Edward Ocran"
DOCS=["Python was created by Guido van Rossum and first released in 1991.","Whisper is a multilingual automatic speech recognition model.","Paris is the capital and largest city of France."]
def run_demo(fast:bool|None=None,audio:Path|None=None,model:Path|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast
    question="Who created Python?" if fast else transcribe_vosk(audio,model or ROOT/".models"/"vosk-model-small-en-us-0.15")
    memory=VectorMemory();[memory.memorize(doc,f"document-{i}",300) for i,doc in enumerate(DOCS,1)];passages=memory.query(question,2)
    answer=summarize_text(passages[0]["text"],1)
    return {"project":69,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","transcript":question,"answer":answer,"passages":passages,"metrics":{"documents":3,"retrieved":2,"best_similarity":passages[0]["score"]}}
def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--audio",type=Path);p.add_argument("--model",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(audio=a.audio,model=a.model);print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
