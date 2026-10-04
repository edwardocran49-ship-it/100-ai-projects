# Dimensionality Reduction with t-SNE: an evidence-led assessment

**Author:** Edward Ocran  
**Project:** 24  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The t-SNE map achieves a 0.4818 class silhouette, revealing substantial visual separation among the ten digit classes.
- **Senior analyst's read:** The embedding is effective for visual exploration, but t-SNE deliberately distorts global distance to preserve local neighborhoods. Nearby clusters are informative; the distance between far-apart clusters should not be interpreted as a quantitative class relationship.
- **Decision:** Use the map to locate confusion neighborhoods and keep downstream modeling in the original feature space.

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

The first chart isolates the primary evaluation result so it is not diluted by unrelated metrics. It should be read using the unit shown on the axis; rates are displayed on a common percentage scale, while errors remain in their original business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

The second chart provides the comparison or experimental context that materially changes the interpretation. It is not a decorative project-count graphic: it shows the baseline, retained information, class balance, error reduction, or evaluation scale needed to understand the result.

## What the Evidence Says

The t-SNE map achieves a 0.4818 class silhouette, revealing substantial visual separation among the ten digit classes.

The embedding is effective for visual exploration, but t-SNE deliberately distorts global distance to preserve local neighborhoods. Nearby clusters are informative; the distance between far-apart clusters should not be interpreted as a quantitative class relationship.

The strongest conclusion is therefore bounded: the project demonstrates measurable signal under its stated design, but the result should only be extended to new populations or operating conditions after the recommended validation is completed.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

These limitations do not erase the result. They define where the evidence is reliable and where a decision-maker would still be taking unmeasured risk.

## Recommendations

1. Use the map to locate confusion neighborhoods and keep downstream modeling in the original feature space.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
