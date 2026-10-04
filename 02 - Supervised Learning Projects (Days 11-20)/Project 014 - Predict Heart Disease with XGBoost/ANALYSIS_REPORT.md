# Predict Heart Disease with XGBoost — Analysis Report

**Author:** Edward Ocran  
**Project:** 14  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The boosted model reaches 97.07% accuracy and 99.00% ROC AUC on the holdout split.
- AUC is the stronger result because it evaluates ranking across thresholds. The duplicated records in the source can make a random split optimistic if near-identical cases cross the train-test boundary, so deduplication and patient-level separation are essential checks.
- **Recommended action:** Deduplicate, calibrate probabilities, and select thresholds around clinical false-negative cost.

## Analytical Question

Can gradient-boosted trees rank heart-disease risk from the supplied clinical attributes?

## Data and Evaluation Design

The heart-disease table contains 1,025 labeled records. An XGBoost classifier with bounded depth, subsampling, and column sampling is trained on a stratified 80% split. Accuracy, precision, recall, F1, and ROC AUC are calculated on the holdout.

## Results

| Measure | Result |
|---|---:|
| Records | 1,025 |
| Accuracy | 97.07% |
| Precision | 97.14% |
| Recall | 97.14% |
| F1 | 97.14% |
| ROC AUC | 99.00% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

![Benchmark and analytical context](analysis/context.png)

## What the Evidence Says

AUC is the stronger result because it evaluates ranking across thresholds. The duplicated records in the source can make a random split optimistic if near-identical cases cross the train-test boundary, so deduplication and patient-level separation are essential checks.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Deduplicate, calibrate probabilities, and select thresholds around clinical false-negative cost.
2. Extend the validation with stronger baselines and segmented error analysis.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- The committed figures correspond to the measured results documented in this report.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
