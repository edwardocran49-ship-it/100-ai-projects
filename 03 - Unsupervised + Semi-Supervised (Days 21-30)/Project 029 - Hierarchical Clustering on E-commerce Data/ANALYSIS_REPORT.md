# Hierarchical Clustering on E-commerce Data — Analysis Report

**Author:** Edward Ocran  
**Project:** 29  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- Five customer clusters achieve a 0.6642 silhouette score among the top 2,000 customers by spend, indicating strong separation within that selected population.
- The high score is encouraging, but the top-spender filter shapes the geometry and excludes the long tail. The clusters describe high-value customer behavior—spend, frequency, basket size, and recency—not the full customer base.
- **Recommended action:** Profile cluster economics and repeat the analysis on the complete customer population before activation.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Customers analyzed | 2,000 |
| Clusters | 5 |
| Silhouette | 0.6642 |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

Five customer clusters achieve a 0.6642 silhouette score among the top 2,000 customers by spend, indicating strong separation within that selected population.

The high score is encouraging, but the top-spender filter shapes the geometry and excludes the long tail. The clusters describe high-value customer behavior—spend, frequency, basket size, and recency—not the full customer base.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Profile cluster economics and repeat the analysis on the complete customer population before activation.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
