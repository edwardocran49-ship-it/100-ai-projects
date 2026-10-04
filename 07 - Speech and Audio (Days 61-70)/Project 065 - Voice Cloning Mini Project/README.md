# Project 65: Voice Cloning Mini Project

**Author:** Edward Ocran  
**Category:** Speech and Audio (Days 61–70)

## Objective

Synthesize approved text in a consented reference voice using Coqui YourTTS.

## Included

- `main.py` — runnable implementation of the PDF workflow.
- `test_project.py` — behavior-focused automated test.
- `ANALYSIS_REPORT.md` — observed results, charts, and interpretation.
- `INPUTS.md` — audio source and handling notes.
- `analysis_assets/` — rendered evidence used by the report.

## Run

```powershell
pip install -r requirements.txt
python main.py --help
python -m unittest -v test_project.py
```

Model weights and downloaded audio are kept out of version control. The course PDF is not redistributed.
