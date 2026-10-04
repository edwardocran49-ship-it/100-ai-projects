# Project 031: Sentiment Analysis with BERT

**Author:** Edward Ocran
**Category:** NLP Projects (Days 31–40)

## Objective

Evaluate a pretrained DistilBERT sentiment classifier on a balanced sample of real IMDb reviews.

## Evidence and inputs

Kaggle IMDb Dataset of 50K Movie Reviews. The default execution uses the actual model or training pipeline described by the course. Fast validation is available to CI so repository checks do not repeatedly download large model weights.

## Included files

- `main.py` — runnable implementation and JSON CLI output
- `test_project.py` — project-specific behavior checks
- `requirements.txt` — runtime dependencies
- `ANALYSIS_REPORT.md` — measured findings with two rendered charts
- `charts/` — report figures
- `DATASET.md` and `download_data.py` — source provenance and retrieval

## Run

```powershell
python -m pip install -r requirements.txt
python main.py
python -m unittest -v test_project.py
```

Run `python download_data.py` first, then `python main.py`.

See [ANALYSIS_REPORT.md](ANALYSIS_REPORT.md) for the evaluated result, interpretation, charts, and reproducibility notes.
