"""Local speech recognition helpers backed by Vosk."""
from __future__ import annotations
import json
from pathlib import Path

from portfolio_core.audio import load_wav


def transcribe_vosk(audio_path: str | Path, model_path: str | Path) -> str:
    from vosk import KaldiRecognizer, Model, SetLogLevel
    SetLogLevel(-1)
    rate, samples = load_wav(audio_path, 16000)
    pcm=(samples.clip(-1,1)*32767).astype("int16").tobytes()
    recognizer=KaldiRecognizer(Model(str(model_path)),rate)
    words=[]
    for index in range(0,len(pcm),8000):
        if recognizer.AcceptWaveform(pcm[index:index+8000]):
            words.append(json.loads(recognizer.Result()).get("text",""))
    words.append(json.loads(recognizer.FinalResult()).get("text",""))
    return " ".join(part for part in words if part).strip()


def stream_transcribe_vosk(audio_path: str | Path, model_path: str | Path, chunk_bytes: int = 8000) -> list[str]:
    """Feed PCM in live-sized chunks and return finalized recognition segments."""
    from vosk import KaldiRecognizer, Model, SetLogLevel
    SetLogLevel(-1)
    rate,samples=load_wav(audio_path,16000);pcm=(samples.clip(-1,1)*32767).astype("int16").tobytes()
    recognizer=KaldiRecognizer(Model(str(model_path)),rate);segments=[]
    for index in range(0,len(pcm),chunk_bytes):
        if recognizer.AcceptWaveform(pcm[index:index+chunk_bytes]):
            text=json.loads(recognizer.Result()).get("text","").strip()
            if text:segments.append(text)
    final=json.loads(recognizer.FinalResult()).get("text","").strip()
    if final:segments.append(final)
    return segments


def score_vosk_language(audio_path: str | Path, model_path: str | Path) -> dict:
    """Return local recognition text and average word confidence for one language model."""
    from vosk import KaldiRecognizer, Model, SetLogLevel
    SetLogLevel(-1);rate,samples=load_wav(audio_path,16000);pcm=(samples.clip(-1,1)*32767).astype("int16").tobytes()
    recognizer=KaldiRecognizer(Model(str(model_path)),rate);recognizer.SetWords(True);recognizer.AcceptWaveform(pcm)
    result=json.loads(recognizer.FinalResult());words=result.get("result",[])
    return {"text":result.get("text","").strip(),"confidence":round(sum(w.get("conf",0) for w in words)/max(len(words),1),4),"words":len(words)}
