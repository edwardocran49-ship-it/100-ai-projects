# Project 25: Self-Supervised Pretraining on Images

**Author:** Edward Ocran  
**Category:** 03 - Unsupervised + Semi-Supervised (Days 21-30)  
**Implementation type:** Vision

## Objective

Use a self-supervised learning task (image rotation prediction) to pretrain a model

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

- `pip install tensorflow numpy matplotlib`

## Success criteria

The command exits successfully, returns `status: ok`, includes task metrics, and passes the included smoke test.
