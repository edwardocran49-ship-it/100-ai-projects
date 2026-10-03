# Project 31: Sentiment Analysis with BERT

**Author:** Edward Ocran  
**Category:** 04 - NLP Projects (Days 31-40)  
**Implementation type:** Nlp

## Objective

Fine-tune or use a pre-trained BERT model for sentiment classification on text data

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

- `pip install transformers datasets torch scikit-learn pandas`

## Success criteria

The command exits successfully, returns `status: ok`, includes task metrics, and passes the included smoke test.
