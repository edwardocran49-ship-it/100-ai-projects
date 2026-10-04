# Project 66: Real-Time Audio Transcriber

**Author:** Edward Ocran
**Category:** Speech and Audio (Days 61–70)

## Objective

Process audio incrementally and return live-style transcription segments.

## Included

- `main.py` — runnable implementation of the PDF workflow.
- `test_project.py` — behavior-focused automated test.
- `ANALYSIS_REPORT.md` — observed results, charts, and interpretation.
- `INPUTS.md` — validation-audio source and handling notes.
- `analysis_assets/` — rendered evidence used by the report.

## Run

```powershell
pip install -r requirements.txt
python main.py --help
python -m unittest -v test_project.py
```

Model weights and downloaded audio are kept out of version control. The course PDF is not redistributed.
