# Voice Gender Classifier — Analysis Report

**Author:** Edward Ocran  
**Project:** 16  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The voice classifier records 97.16% holdout accuracy on the supplied acoustic-feature table.
- The high score is evidence that the engineered frequency features separate the dataset labels well. It should not be generalized to gender identity or deployed on unseen microphones, languages, age groups, or recording conditions without broader validation.
- **Recommended action:** Test speaker-disjoint splits and report calibration and subgroup performance.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Samples | 3,168 |
| Holdout accuracy | 98.42% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

The voice classifier records 97.16% holdout accuracy on the supplied acoustic-feature table.

The high score is evidence that the engineered frequency features separate the dataset labels well. It should not be generalized to gender identity or deployed on unseen microphones, languages, age groups, or recording conditions without broader validation.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Test speaker-disjoint splits and report calibration and subgroup performance.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
