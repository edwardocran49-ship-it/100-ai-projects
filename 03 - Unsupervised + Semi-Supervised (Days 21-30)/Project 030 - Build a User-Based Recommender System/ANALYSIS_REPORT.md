# Build a User-Based Recommender System — Analysis Report

**Author:** Edward Ocran  
**Project:** 30  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- User-based collaborative filtering records 1.0476-star RMSE across 610 leave-one-out user ratings.
- The typical error is about 23% of the full 0.5-to-5 rating range. That is a credible baseline, but ranking quality matters more than rating reconstruction for recommendations; popular-item and global-mean baselines are also needed to establish incremental value.
- **Recommended action:** Add baseline RMSE, Precision@K, Recall@K, and cold-start coverage before judging recommendation quality.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Ratings | 100,836 |
| Users | 610 |
| Leave-one-out RMSE | 1.0476 stars |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

User-based collaborative filtering records 1.0476-star RMSE across 610 leave-one-out user ratings.

The typical error is about 23% of the full 0.5-to-5 rating range. That is a credible baseline, but ranking quality matters more than rating reconstruction for recommendations; popular-item and global-mean baselines are also needed to establish incremental value.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Add baseline RMSE, Precision@K, Recall@K, and cold-start coverage before judging recommendation quality.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
