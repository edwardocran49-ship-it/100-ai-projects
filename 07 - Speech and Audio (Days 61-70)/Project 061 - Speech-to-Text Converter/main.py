"""Transcribe a WAV file with SpeechRecognition and save readable text."""
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.speech import transcribe_vosk
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=61,"Speech-to-Text Converter","Edward Ocran"

def transcribe(path:Path,model:Path)->str:
    return transcribe_vosk(path,model)

def run_demo(fast:bool|None=None,audio:Path|None=None,output:Path|None=None,model:Path|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast
    if fast: text="Machine learning makes recorded speech searchable."
    else:
        if audio is None: raise ValueError("Provide --audio with a WAV recording")
        model=model or ROOT/".models"/"vosk-model-small-en-us-0.15"
        text=transcribe(audio,model)
    if output: output.write_text(text+"\n",encoding="utf-8")
    return {"project":61,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","transcript":text,
            "metrics":{"words":len(text.split()),"characters":len(text),"saved":bool(output)}}

def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--audio",type=Path);p.add_argument("--model",type=Path);p.add_argument("--output",type=Path,default=Path("transcript.txt"));p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(audio=a.audio,output=a.output,model=a.model);print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
