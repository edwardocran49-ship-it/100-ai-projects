# Analysis Report: PCA for Dimensionality Reduction

**Author:** Edward Ocran  
**Project:** 8  
**Run status:** Verified locally

## Question

How much of the digits dataset can two principal components preserve?

## Data used

All 1,797 digit images were standardized across their 64 pixel features before PCA.

## Method

PCA reduced the standardized vectors from 64 dimensions to two. The retained variance ratio is the key diagnostic.

## Results

| Measure | Result |
|---|---:|
| Images | 1,797 |
| Input dimensions | 64 |
| Output dimensions | 2 |
| Variance retained | 21.59% |

## What the result means

Two components retain only about one fifth of the standardized variance. The projection is suitable for visualization, but it discards too much information to replace the full feature set in a high-accuracy recognizer.

## Limitations

Variance is not the same as class separation, and linear PCA cannot unfold nonlinear structure. The current run does not compare downstream classifier accuracy before and after reduction.

## Next step

Plot the two-dimensional embedding by digit, compare with t-SNE, and measure classification accuracy across several component counts.
