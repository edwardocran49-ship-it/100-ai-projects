# Analysis Report: Logistic Regression on Titanic Dataset

**Author:** Edward Ocran  
**Project:** 2  
**Run status:** Verified locally

## Question

Can basic passenger information recover a useful Titanic survival baseline?

## Data used

The Kaggle file contains 1,309 passengers. Age and fare were median-imputed; categorical gaps were filled with the most frequent value. The model used age, fare, sex, siblings/spouses, parents/children, class, and embarkation port.

## Method

Numeric fields were standardized, categorical fields one-hot encoded, and a logistic regression was trained on a stratified 80% split.

## Results

| Measure | Result |
|---|---:|
| Passengers | 1,309 |
| Holdout accuracy | 74.81% |

## What the result means

The model classified about three quarters of the holdout passengers correctly. That is a credible first baseline, but accuracy alone hides which survivors were missed. Class and sex are strong historical correlates, so the score should not be mistaken for a generally transferable safety model.

## Limitations

This copy combines train and test-style records and uses a single random holdout. It does not report recall by class or demographic group, and several potentially informative fields are absent from the selected feature set.

## Next step

Add precision, recall, and a confusion matrix; engineer family-size and title features; then compare cross-validated logistic and tree models.
