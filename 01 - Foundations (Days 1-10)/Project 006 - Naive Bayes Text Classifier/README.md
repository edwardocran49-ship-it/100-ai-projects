# Project 6: Naive Bayes Text Classifier

**Author:** Edward Ocran  
**Category:** 01 - Foundations (Days 1-10)  
**Implementation type:** Nlp

## Objective

Build a spam detector using the Multinomial Naive Bayes algorithm on a text dataset.

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

- `pip install pandas scikit-learn matplotlib seaborn`

## Success criteria

The command exits successfully, returns `status: ok`, includes task metrics, and passes the included smoke test.
