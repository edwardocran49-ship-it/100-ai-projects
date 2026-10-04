# K-Means Clustering for Customer Segmentation — Analysis Report

**Author:** Edward Ocran  
**Project:** 3  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- Five income-spending segments achieve a 0.5547 silhouette score, indicating useful but not perfect separation.
- The geometry supports distinct customer groups, yet nearly half of the theoretical separation range remains unresolved. These clusters are best treated as hypotheses for targeting, then validated against purchase frequency, margin, or campaign response.
- **Recommended action:** Use the segments for exploratory targeting tests, not as permanent customer labels.

## Analytical Question

Do annual income and spending score form distinct customer segments?

## Data and Evaluation Design

The Mall Customers file supplies annual income and spending score for 200 customers. Both variables are standardized. K-means is fitted for one through ten clusters to produce the elbow series, after which the course-selected five-cluster solution is evaluated with silhouette score.

## Results

| Measure | Result |
|---|---:|
| Customers | 200 |
| Selected clusters | 5 |
| Silhouette score | 0.5547 |
| Inertia at k=1 | 400.000 |
| Inertia at k=5 | 65.568 |
| Inertia at k=10 | 29.686 |

## Visual Evidence

![Verified model performance](analysis/performance.png)

![Benchmark and analytical context](analysis/context.png)

## What the Evidence Says

The geometry supports distinct customer groups, yet nearly half of the theoretical separation range remains unresolved. These clusters are best treated as hypotheses for targeting, then validated against purchase frequency, margin, or campaign response.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Use the segments for exploratory targeting tests, not as permanent customer labels.
2. Extend the validation with stronger baselines and segmented error analysis.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
