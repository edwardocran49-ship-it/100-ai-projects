# Project 035: Resume Parser

**Author:** Edward Ocran
**Category:** NLP Projects (Days 31–40)

## Objective

Extract contact details, skills, education, and experience from TXT or PDF resumes.

## Evidence and inputs

Included fictional sample resume; accepts user TXT/PDF files. The default execution uses the actual model or training pipeline described by the course. Fast validation is available to CI so repository checks do not repeatedly download large model weights.

## Included files

- `main.py` — runnable implementation and JSON CLI output
- `test_project.py` — project-specific behavior checks
- `requirements.txt` — runtime dependencies
- `ANALYSIS_REPORT.md` — measured findings with two rendered charts
- `charts/` — report figures
- `INPUTS.md` and `data/sample_resume.txt` — documented sample input

## Run

```powershell
python -m pip install -r requirements.txt
python main.py
python -m unittest -v test_project.py
```

Run `python main.py` or pass a resume path.

See [ANALYSIS_REPORT.md](ANALYSIS_REPORT.md) for the evaluated result, interpretation, charts, and reproducibility notes.
