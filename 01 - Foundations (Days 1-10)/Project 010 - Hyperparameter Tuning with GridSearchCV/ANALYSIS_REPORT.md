# Analysis Report: Hyperparameter Tuning with GridSearchCV

**Author:** Edward Ocran  
**Project:** 10  
**Run status:** Verified locally

## Question

Which small SVM configuration works best for Iris classification?

## Data used

The complete Iris dataset provides 150 flowers, four measurements, and three balanced species.

## Method

A standardized SVM pipeline was tuned with five-fold grid search over kernel, `C`, and gamma, then evaluated on a stratified 20% holdout.

## Results

| Measure | Result |
|---|---:|
| Samples | 150 |
| Holdout accuracy | 93.33% |
| Best kernel | linear |
| Best C | 0.1 |

## What the result means

The selected model is a strongly regularized linear SVM. On this split, extra RBF flexibility was unnecessary; the flower measurements are already close to linearly separable for the tested grid.

## Limitations

Thirty holdout cases make the reported accuracy sensitive to a few predictions. The grid is intentionally small and the final holdout is evaluated only once.

## Next step

Repeat the outer evaluation with nested cross-validation and inspect the species-level confusion matrix.
