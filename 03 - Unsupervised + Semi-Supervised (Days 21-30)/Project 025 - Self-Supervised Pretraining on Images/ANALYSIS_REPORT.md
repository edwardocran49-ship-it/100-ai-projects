# Self-Supervised Pretraining on Images — Analysis Report

**Author:** Edward Ocran  
**Project:** 25  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- With only 800 labeled training images, the PCA representation supports 81.25% holdout accuracy while retaining 86.56% of image variance.
- The result shows useful label efficiency: unsupervised structure learned from 8,000 images allows a linear classifier to operate with labels for only one in ten training images. The gap to fully supervised performance quantifies the price of limited labels and linear compression.
- **Recommended action:** Build a label-budget curve to show accuracy gained per additional labeled image.

## Analytical Question

What does the verified model result reveal, and how should it be used?

## Data and Evaluation Design





The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

| Measure | Result |
|---|---:|
| Images | 10,000 |
| Labeled training images | 800 |
| Variance retained | 86.56% |
| Accuracy | 81.25% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

With only 800 labeled training images, the PCA representation supports 81.25% holdout accuracy while retaining 86.56% of image variance.

The result shows useful label efficiency: unsupervised structure learned from 8,000 images allows a linear classifier to operate with labels for only one in ten training images. The gap to fully supervised performance quantifies the price of limited labels and linear compression.

## Risks and Limitations

The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment.

## Recommendations

1. Build a label-budget curve to show accuracy gained per additional labeled image.
2. Extend the validation with stronger baselines and segmented error analysis.
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
