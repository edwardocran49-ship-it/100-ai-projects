# Dimensionality Reduction with t-SNE — Analysis Report

**Author:** Edward Ocran  
**Project:** 24  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The t-SNE map achieves a 0.4818 class silhouette, revealing substantial visual separation among the ten digit classes.
- The embedding is effective for visual exploration, but t-SNE deliberately distorts global distance to preserve local neighborhoods. Nearby clusters are informative; the distance between far-apart clusters should not be interpreted as a quantitative class relationship.
- **Recommended action:** Use the map to locate confusion neighborhoods and keep downstream modeling in the original feature space.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Images | 1,797 |
| Class silhouette | 0.4818 |
| KL divergence | 0.8463 |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

The t-SNE map achieves a 0.4818 class silhouette, revealing substantial visual separation among the ten digit classes.

The embedding is effective for visual exploration, but t-SNE deliberately distorts global distance to preserve local neighborhoods. Nearby clusters are informative; the distance between far-apart clusters should not be interpreted as a quantitative class relationship.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Use the map to locate confusion neighborhoods and keep downstream modeling in the original feature space.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
