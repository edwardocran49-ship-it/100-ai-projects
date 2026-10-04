# SVM for Handwritten Digit Recognition — Analysis Report

**Author:** Edward Ocran  
**Project:** 7  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The RBF SVM classifies 98.06% of holdout digits correctly—an 88-point lift over random ten-class choice.
- Performance is strong enough that aggregate accuracy no longer reveals the main opportunity. Error concentration by digit pair and robustness to shifts, blur, and rotation will provide more useful information than another decimal place of accuracy.
- **Recommended action:** Preserve this benchmark and focus the next iteration on error taxonomy and robustness.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Images | 1,797 |
| Holdout accuracy | 98.06% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

The RBF SVM classifies 98.06% of holdout digits correctly—an 88-point lift over random ten-class choice.

Performance is strong enough that aggregate accuracy no longer reveals the main opportunity. Error concentration by digit pair and robustness to shifts, blur, and rotation will provide more useful information than another decimal place of accuracy.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Preserve this benchmark and focus the next iteration on error taxonomy and robustness.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
