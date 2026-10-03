# Project 11: Predict Stock Prices with LSTM

**Author:** Edward Ocran  
**Category:** 02 - Supervised Learning Projects (Days 11-20)  
**Implementation type:** Regression

## Objective

Use an LSTM neural network to predict the closing price of a stock using its past data.

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

- `pip install pandas yfinance scikit-learn matplotlib tensorflow`

## Success criteria

The command exits successfully, returns `status: ok`, includes task metrics, and passes the included smoke test.
