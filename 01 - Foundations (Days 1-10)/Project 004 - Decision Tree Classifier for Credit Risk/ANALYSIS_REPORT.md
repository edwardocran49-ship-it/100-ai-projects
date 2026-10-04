# Decision Tree Classifier for Credit Risk — Analysis Report

**Author:** Edward Ocran  
**Project:** 4  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The 70% headline accuracy only matches the majority-class baseline, so the current tree does not yet demonstrate incremental decision value.
- This is the most important finding in the project: a seemingly acceptable accuracy can be operationally empty. Credit decisions require class-specific recall, cost-weighted errors, calibration, and fairness checks; none can be replaced by overall accuracy.
- **Recommended action:** Do not advance this specification until it beats the majority rule on cost-sensitive and class-level measures.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Applicants | 1,000 |
| Holdout accuracy | 70.00% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

The 70% headline accuracy only matches the majority-class baseline, so the current tree does not yet demonstrate incremental decision value.

This is the most important finding in the project: a seemingly acceptable accuracy can be operationally empty. Credit decisions require class-specific recall, cost-weighted errors, calibration, and fairness checks; none can be replaced by overall accuracy.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Do not advance this specification until it beats the majority rule on cost-sensitive and class-level measures.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
