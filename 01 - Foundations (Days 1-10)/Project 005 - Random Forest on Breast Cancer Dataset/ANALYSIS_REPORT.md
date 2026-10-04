# Analysis Report: Random Forest on Breast Cancer Dataset

**Author:** Edward Ocran  
**Project:** 5  
**Run status:** Verified locally

## Question

How accurately can a random forest classify the Wisconsin diagnostic measurements?

## Data used

The built-in scikit-learn copy contains 569 observations with thirty numeric features. The split was stratified to preserve the malignant/benign balance.

## Method

A 150-tree random forest was trained with a fixed seed and evaluated on a 20% holdout.

## Results

| Measure | Result |
|---|---:|
| Samples | 569 |
| Holdout accuracy | 95.61% |

## What the result means

The model correctly classified roughly 96% of the holdout set, which is strong for a compact baseline. A medical screening context would still care more about malignant-case recall than overall accuracy.

## Limitations

The sample is small, comes from one historical source, and the current report does not include sensitivity, specificity, calibration, or external validation. It is not a diagnostic device.

## Next step

Add a confusion matrix and ROC curve, tune the threshold for malignant recall, and validate on an independent cohort.
