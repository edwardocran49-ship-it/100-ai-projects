# Naive Bayes Text Classifier — Analysis Report

**Author:** Edward Ocran  
**Project:** 6  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- Overall accuracy is 96.86%, but spam F1 is lower at 86.69%; the minority class remains the real analytical challenge.
- The ten-point gap between accuracy and spam F1 is a classic imbalance effect. The model is strong at preserving legitimate messages, but the business risk sits in missed scams and legitimate messages incorrectly quarantined.
- **Recommended action:** Tune thresholds and compare character n-grams using false-positive and false-negative costs.

## Analytical Question

Can TF-IDF word evidence separate spam from legitimate SMS messages?

## Data and Evaluation Design

The SMS Spam Collection contains 5,572 labeled messages. English stop words are removed with TF-IDF, and a Multinomial Naive Bayes classifier is fitted on a stratified 80% split. The report keeps the spam class visible through precision, recall, F1, and confusion counts rather than relying on accuracy alone.

## Results

| Measure | Result |
|---|---:|
| Messages | 5,572 |
| Accuracy | 96.86% |
| Spam precision | 100.00% |
| Spam recall | 76.51% |
| Spam F1 | 86.69% |
| False spam alarms / missed spam | 0 / 35 |

## Visual Evidence

![Verified model performance](analysis/performance.png)

![Benchmark and analytical context](analysis/context.png)

## What the Evidence Says

The ten-point gap between accuracy and spam F1 is a classic imbalance effect. The model is strong at preserving legitimate messages, but the business risk sits in missed scams and legitimate messages incorrectly quarantined.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Tune thresholds and compare character n-grams using false-positive and false-negative costs.
2. Extend the validation with stronger baselines and segmented error analysis.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
