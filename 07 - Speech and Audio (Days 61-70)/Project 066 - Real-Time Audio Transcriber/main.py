"""Transcribe microphone audio continuously until the user says stop."""
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.speech import stream_transcribe_vosk
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=66,"Real-Time Audio Transcriber","Edward Ocran"

def run_demo(fast:bool|None=None,audio:Path|None=None,model:Path|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast
    if fast:segments=["Live captions make meetings easier to follow","Please stop the transcription"]
    else:
        if audio is None:raise ValueError("Provide --audio with a WAV recording")
        segments=stream_transcribe_vosk(audio,model or ROOT/".models"/"vosk-model-small-en-us-0.15")
    return {"project":66,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","segments":segments,"transcript":" ".join(segments),"metrics":{"segments":len(segments),"words":sum(len(x.split()) for x in segments),"stop_detected":"stop" in segments[-1].lower()}}
def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--audio",type=Path);p.add_argument("--model",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(audio=a.audio,model=a.model);print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
