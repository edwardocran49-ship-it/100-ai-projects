# Project 11: Predict Stock Prices with LSTM

**Author:** Edward Ocran  
**Category:** 02 - Supervised Learning Projects (Days 11-20)

## Objective

Train and evaluate the named model on the real source identified by the course project. The executable reports the source name, actual row count, and holdout metrics.

## Dataset

See [DATASET.md](DATASET.md). Run `python download_data.py` to fetch or refresh the source without placing large or restricted data in Git.

## Analysis

Read the verified findings in [ANALYSIS_REPORT.md](ANALYSIS_REPORT.md).

## Run

```powershell
python -m pip install -r requirements.txt
python main.py
python -m unittest -v test_project.py
```

The default run uses a bounded sample for very large datasets so it remains practical on a laptop while still training on genuine records.
