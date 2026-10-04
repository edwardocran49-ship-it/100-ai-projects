# Project 033: Question Answering System

**Author:** Edward Ocran
**Category:** NLP Projects (Days 31–40)

## Objective

Extract an evidence span and confidence score from a supplied context with a SQuAD-trained transformer.

## Evidence and inputs

Embedded factual context and question. The default execution uses the actual model or training pipeline described by the course. Fast validation is available to CI so repository checks do not repeatedly download large model weights.

## Included files

- `main.py` — runnable implementation and JSON CLI output
- `test_project.py` — project-specific behavior checks
- `requirements.txt` — runtime dependencies
- `ANALYSIS_REPORT.md` — measured findings with two rendered charts
- `charts/` — report figures

## Run

```powershell
python -m pip install -r requirements.txt
python main.py
python -m unittest -v test_project.py
```

Run `python main.py`.

See [ANALYSIS_REPORT.md](ANALYSIS_REPORT.md) for the evaluated result, interpretation, charts, and reproducibility notes.

## Inputs

See [INPUTS.md](INPUTS.md) for the input type, evaluation fixtures, and privacy boundary.
