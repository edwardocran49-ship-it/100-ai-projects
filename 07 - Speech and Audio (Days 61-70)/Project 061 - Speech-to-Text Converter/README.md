# Project 61: Speech-to-Text Converter

**Author:** Edward Ocran  
**Category:** 07 - Speech and Audio (Days 61-70)  
**Implementation type:** Nlp

## Objective

Build a tool that takes audio input (live or file) and converts it into accurate, readable

## What is included

- `main.py` - deterministic, offline runnable implementation.
- `test_project.py` - automated smoke test.
- `course-requirements.txt` - dependency commands mentioned by the course, when present.
- The licensed course PDFs are intentionally excluded from this public repository.

## Run

```powershell
python main.py
python -m unittest -v test_project.py
```

The default demo uses generated sample data so it runs without API keys, paid services, or large model downloads. Replace the sample data with the dataset or service described in the PDF when extending the project.

## Course dependency guidance

- `pip install openai-whisper speechrecognition pydub`

## Success criteria

The command exits successfully, returns `status: ok`, includes task metrics, and passes the included smoke test.
