# Analysis Report: Decision Tree Classifier for Credit Risk

**Author:** Edward Ocran  
**Project:** 4  
**Run status:** Verified locally

## Question

Can a shallow decision tree separate good and bad credit outcomes in the German Credit data?

## Data used

The run used 1,000 applicants from the target-bearing Kaggle version of German Credit. Missing account categories were imputed and categorical variables one-hot encoded.

## Method

A decision tree capped at depth five was trained on a stratified 80/20 split. The depth cap trades some fit for a model that remains inspectable.

## Results

| Measure | Result |
|---|---:|
| Applicants | 1,000 |
| Holdout accuracy | 70.00% |

## What the result means

Seven correct decisions out of ten is only a baseline. In credit risk, the cost of approving a bad loan differs from rejecting a good applicant, so accuracy is not enough to judge operational usefulness.

## Limitations

The dataset is small and dated, and this run does not tune class weights or decision thresholds. It also does not audit performance by sex, age, or housing status, which is essential before any consequential use.

## Next step

Report class-specific recall and cost-weighted error, run fairness checks, and compare calibrated logistic regression and gradient boosting.
