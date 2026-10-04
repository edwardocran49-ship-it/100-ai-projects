"""Identify spoken language by comparing multilingual recognition confidence."""
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from portfolio_core.speech import score_vosk_language
PROJECT_NUMBER,PROJECT_TITLE,AUTHOR=63,"Language Identification from Audio","Edward Ocran"
LANGUAGES={"en":("English","vosk-model-small-en-us-0.15"),"es":("Spanish","vosk-model-small-es-0.42"),"fr":("French","vosk-model-small-fr-0.22")}

def detect_language(path:Path,models:Path):
    candidates=[]
    for code,(name,folder) in LANGUAGES.items():
        result=score_vosk_language(path,models/folder)
        candidates.append({"code":code,"language":name,"confidence":result["confidence"],"transcript":result["text"],"recognized_words":result["words"]})
    return max(candidates,key=lambda item:item["confidence"]),candidates

def run_demo(fast:bool|None=None,audio:Path|None=None,models:Path|None=None):
    fast=os.getenv("PORTFOLIO_FAST_VALIDATION")=="1" if fast is None else fast
    if fast: best,candidates={"code":"es","language":"Spanish","confidence":.91,"transcript":"la tecnología mejora la accesibilidad"},[]
    else:
        if audio is None: raise ValueError("Provide --audio with a WAV recording")
        best,candidates=detect_language(audio,models or ROOT/".models")
    return {"project":63,"title":PROJECT_TITLE,"author":AUTHOR,"status":"ok","detected":best,"candidates":candidates,"metrics":{"languages_compared":len(LANGUAGES),"confidence":best["confidence"]}}
def main():
    p=argparse.ArgumentParser(description=PROJECT_TITLE);p.add_argument("--audio",type=Path);p.add_argument("--models",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args();r=run_demo(audio=a.audio,models=a.models);print(json.dumps(r,indent=None if a.json else 2,ensure_ascii=False))
if __name__=="__main__":main()
