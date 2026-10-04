"""Create speech audio from text with an offline system voice."""
from __future__ import annotations
import argparse,json,os,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.audio import wav_metrics,write_tone
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=62,"Text-to-Speech with ElevenLabs or Coqui","Edward Ocran"

def synthesize(text:str,output:Path,voice:str|None=None,rate:int=175,backend:str="system"):
    if backend=="coqui":
        from TTS.api import TTS
        engine=TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC",progress_bar=False)
        engine.tts_to_file(text=text,file_path=str(output));return
    if backend=="elevenlabs":
        from elevenlabs.client import ElevenLabs
        client=ElevenLabs();audio=client.text_to_speech.convert(text=text,voice_id=voice or "Rachel",model_id="eleven_multilingual_v2")
        output.write_bytes(b"".join(audio));return
    import pyttsx3
    engine=pyttsx3.init(); engine.setProperty("rate",rate)
    if voice:
        match=next((v for v in engine.getProperty("voices") if voice.lower() in v.name.lower()),None)
        if match: engine.setProperty("voice",match.id)
    engine.save_to_file(text,str(output));engine.runAndWait()
    if not output.exists(): raise RuntimeError("Speech engine did not create the output file")

def run_demo(fast:bool|None=None,text="Clear narration makes written information accessible.",output:Path|None=None,backend="system"):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast
    output=output or Path(tempfile.gettempdir())/"project62_narration.wav"
    if fast: write_tone(output,220,.8)
    else: synthesize(text,output,backend=backend)
    return {"project":62,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","backend":backend,"output":str(output),"text":text,"metrics":wav_metrics(output)}
def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("text",nargs="?",default="Clear narration makes written information accessible.");p.add_argument("--backend",choices=["system","coqui","elevenlabs"],default="system");p.add_argument("--output",type=Path,default=Path("narration.wav"));p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(text=a.text,output=a.output,backend=a.backend);print(json.dumps(r,indent=None if a.json else 2))
if __name__=="__main__":main()
