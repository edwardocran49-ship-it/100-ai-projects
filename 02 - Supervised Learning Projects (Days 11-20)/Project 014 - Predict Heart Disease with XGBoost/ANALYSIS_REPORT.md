# Analysis Report: Predict Heart Disease with XGBoost

**Author:** Edward Ocran  
**Project:** 14  
**Run status:** Verified locally

## Question

Can gradient-boosted trees identify heart-disease cases from the supplied clinical attributes?

## Data used

The dataset contains 1,025 records with thirteen predictors and a binary target. The holdout split was stratified.

## Method

XGBoost used 120 shallow trees, moderate shrinkage, and row/column subsampling. Accuracy and ROC AUC were measured on the 20% holdout.

## Results

| Measure | Result |
|---|---:|
| Records | 1,025 |
| Accuracy | 96.59% |
| ROC AUC | 0.9866 |

## What the result means

Both discrimination measures are high on this split. The result is encouraging for the benchmark, but near-duplicate rows in commonly circulated versions of this dataset can make random-split performance look better than real clinical generalization.

## Limitations

There is no external validation, calibration analysis, subgroup audit, or clinical utility study. The program is not medical advice or a diagnostic tool.

## Next step

Check and remove duplicates before splitting, report sensitivity/specificity and calibration, then validate on an independent cohort.
