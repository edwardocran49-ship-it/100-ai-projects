# Logistic Regression on Titanic Dataset — Analysis Report

**Author:** Edward Ocran  
**Project:** 2  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The logistic model reaches 74.81% accuracy, about 13 percentage points above a majority-class rule.
- The lift over the majority baseline confirms that the passenger features contain real predictive structure. The useful next question is not whether the model beats chance, but whether survivor recall and false-negative patterns remain acceptable across passenger groups.
- **Recommended action:** Retain the model as a transparent baseline and evaluate class-level errors before comparing more complex estimators.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Passengers | 1,309 |
| Holdout accuracy | 74.81% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

The logistic model reaches 74.81% accuracy, about 13 percentage points above a majority-class rule.

The lift over the majority baseline confirms that the passenger features contain real predictive structure. The useful next question is not whether the model beats chance, but whether survivor recall and false-negative patterns remain acceptable across passenger groups.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Retain the model as a transparent baseline and evaluate class-level errors before comparing more complex estimators.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
