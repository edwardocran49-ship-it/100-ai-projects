# Predict Stock Prices with LSTM — Analysis Report

**Author:** Edward Ocran  
**Project:** 11  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The sequence model misses the next adjusted close by $4.73 on average across the chronological holdout.
- The dollar error is interpretable but incomplete without a same-period naive forecast. Equity prices are highly persistent, so a complex sequence representation must beat “tomorrow equals today” and survive walk-forward evaluation to demonstrate incremental signal.
- **Recommended action:** Add naive and moving-average benchmarks before making any claim of forecasting advantage.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Trading days | 1,255 |
| Holdout MAE | $4.7309 |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

The sequence model misses the next adjusted close by $4.73 on average across the chronological holdout.

The dollar error is interpretable but incomplete without a same-period naive forecast. Equity prices are highly persistent, so a complex sequence representation must beat “tomorrow equals today” and survive walk-forward evaluation to demonstrate incremental signal.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Add naive and moving-average benchmarks before making any claim of forecasting advantage.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
