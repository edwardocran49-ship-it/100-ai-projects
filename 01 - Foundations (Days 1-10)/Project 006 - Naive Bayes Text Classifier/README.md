# Project 6: Naive Bayes Text Classifier

**Author:** Edward Ocran  
**Category:** 01 - Foundations (Days 1-10)

## Objective

Implement and evaluate the course project with its specified real dataset or, for Project 9, the synthetic observations explicitly required by the from-scratch optimization exercise.

## Data provenance

See [DATASET.md](DATASET.md). The executable reports the dataset name and actual record count, making the input used by the model easy to verify.

## Run

```powershell
python -m pip install -r requirements.txt
python main.py
python -m unittest -v test_project.py
```

The split, model seed, and evaluation are deterministic so results can be reproduced locally and in continuous integration.
