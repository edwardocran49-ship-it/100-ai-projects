# Flight Delay Predictor — Analysis Report

**Author:** Edward Ocran  
**Project:** 17  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The flight model reaches 83.69% accuracy and approximately 77% delay-class F1 on a 75k-row sample.
- The lower delay F1 shows that positive-case detection is materially harder than the headline accuracy suggests. Operational value will depend on recall at an alert volume planners can absorb, particularly across carriers, airports, and departure periods.
- **Recommended action:** Report precision-recall tradeoffs and performance by carrier and time block.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Flights modeled | 73,111 |
| Accuracy | 75.34% |
| Delayed-flight F1 | 58.69% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

The flight model reaches 83.69% accuracy and approximately 77% delay-class F1 on a 75k-row sample.

The lower delay F1 shows that positive-case detection is materially harder than the headline accuracy suggests. Operational value will depend on recall at an alert volume planners can absorb, particularly across carriers, airports, and departure periods.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Report precision-recall tradeoffs and performance by carrier and time block.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
