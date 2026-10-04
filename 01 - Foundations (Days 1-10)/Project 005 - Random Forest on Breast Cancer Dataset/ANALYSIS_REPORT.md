# Random Forest on Breast Cancer Dataset — Analysis Report

**Author:** Edward Ocran  
**Project:** 5  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The forest reaches 95.61% accuracy, roughly 32.9 percentage points above the majority-class baseline.
- The margin over baseline is substantial and supports the value of the diagnostic measurements. For screening, however, the decisive metric is malignant-case sensitivity; a small number of false negatives can matter more than many correct benign classifications.
- **Recommended action:** Move next to sensitivity, specificity, calibration, and external-cohort validation.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Samples | 569 |
| Holdout accuracy | 95.61% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

The forest reaches 95.61% accuracy, roughly 32.9 percentage points above the majority-class baseline.

The margin over baseline is substantial and supports the value of the diagnostic measurements. For screening, however, the decisive metric is malignant-case sensitivity; a small number of false negatives can matter more than many correct benign classifications.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Move next to sensitivity, specificity, calibration, and external-cohort validation.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
