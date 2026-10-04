# Spam Detection with MultinomialNB — Analysis Report

**Author:** Edward Ocran  
**Project:** 19  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The PDF-specified TF-IDF MultinomialNB pipeline reaches 96.86% accuracy and 86.69% spam F1.
- The ten-point gap between headline accuracy and spam F1 shows why minority-class performance must remain visible. This implementation now reproduces the required TF-IDF workflow rather than substituting raw count features.
- **Recommended action:** Retain the required TF-IDF baseline and prioritize class-level error review over headline accuracy.

## Analytical Question

How effectively does the PDF-specified TF-IDF MultinomialNB pipeline detect SMS spam?

## Data and Evaluation Design

The SMS Spam Collection supplies 5,572 labeled messages. Following the PDF, English stop words are removed with a TF-IDF vectorizer and a Multinomial Naive Bayes classifier is trained on a stratified 80% split.

## Results

| Measure | Result |
|---|---:|
| Messages | 5,572 |
| Accuracy | 96.86% |
| Spam F1 | 86.69% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

![Benchmark and analytical context](analysis/context.png)

## What the Evidence Says

The ten-point gap between headline accuracy and spam F1 shows why minority-class performance must remain visible. This implementation now reproduces the required TF-IDF workflow rather than substituting raw count features.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Retain the required TF-IDF baseline and prioritize class-level error review over headline accuracy.
2. Review false positives and missed spam, then tune the decision threshold and validate across repeated shared folds.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- The committed figures correspond to the measured results documented in this report.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
