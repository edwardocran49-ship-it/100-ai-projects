# Project 1: Predict House Prices (Boston Housing Dataset)

**Author:** Edward Ocran  
**Category:** 01 - Foundations (Days 1-10)  
**Implementation type:** Regression

## Objective

Predict the median value of owner-occupied homes from the Boston Housing dataset. The runnable baseline uses average rooms per dwelling (`RM`) to predict median value (`MEDV`) with ordinary least squares.

## Dataset

The repository includes the 506-row `HousingData.csv` downloaded from the Kaggle dataset `altavish/boston-housing-dataset`. Kaggle lists it as CC0: Public Domain. See [DATASET.md](DATASET.md) for provenance, columns, and limitations.

## Analysis

Read the verified findings in [ANALYSIS_REPORT.md](ANALYSIS_REPORT.md).

## Run

```powershell
python main.py
python -m unittest -v test_project.py
```

No third-party Python package is required for the baseline. The program validates the input, performs a deterministic 80/20 split, trains the regression, and reports mean absolute error.

## Success criteria

- Loads at least 500 genuine dataset records.
- Uses `RM` as the feature and `MEDV` as the target.
- Produces a finite holdout MAE below 10.
- Passes the included automated test.
