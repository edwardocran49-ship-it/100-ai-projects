"""Consent-gated voice cloning with a Coqui YourTTS adapter."""
from __future__ import annotations
import argparse,json,os,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.audio import wav_metrics,write_tone
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=65,"Voice Cloning Mini Project","Edward Ocran"

def clone(reference:Path,text:str,output:Path,consent:bool):
    if not consent: raise PermissionError("Recorded speaker consent is required")
    from TTS.api import TTS
    engine=TTS(model_name="tts_models/multilingual/multi-dataset/your_tts",progress_bar=False)
    engine.tts_to_file(text=text,speaker_wav=str(reference),language="en",file_path=str(output))
def run_demo(fast:bool|None=None,reference:Path|None=None,output:Path|None=None,consent=True):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast;temp=Path(tempfile.gettempdir());reference=reference or temp/"project65_reference.wav";output=output or temp/"project65_clone.wav"
    if fast: write_tone(reference,210,1);write_tone(output,214,1)
    else: clone(reference,"This sample was synthesized with the speaker's permission.",output,consent)
    return {"project":65,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","consent_confirmed":consent,"reference":wav_metrics(reference),"output":wav_metrics(output)}
def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--reference",type=Path);p.add_argument("--output",type=Path,default=Path("cloned_voice.wav"));p.add_argument("--consent",action="store_true");p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(reference=a.reference,output=a.output,consent=a.consent);print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
