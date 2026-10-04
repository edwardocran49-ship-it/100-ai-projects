# Analysis Report: Predict House Prices (Boston Housing Dataset)

**Author:** Edward Ocran  
**Project:** 1  
**Run status:** Verified locally

## Question

How much signal does average room count carry for Boston-area home values?

## Data used

The run used 506 Boston Housing records downloaded from Kaggle. Rows with a missing `RM` or `MEDV` value were excluded; more than 500 complete records remained. A seeded 80/20 split kept the comparison reproducible.

## Method

I fitted an ordinary least-squares line with `RM` (average rooms per dwelling) as the sole predictor and `MEDV` as the target. Keeping one feature makes the baseline easy to inspect before adding the other twelve variables.

## Results

| Measure | Result |
|---|---:|
| Usable records | 506 |
| Holdout MAE | 4.0726 |
| Fitted slope | 9.0887 |

## What the result means

The fitted slope says that one additional room is associated with roughly $9,100 higher median value in this one-variable model. The holdout error is about $4,073 because `MEDV` is expressed in thousands of dollars. That is useful as a baseline, but not accurate enough to treat room count as a complete valuation model.

## Limitations

The dataset is old, geographically narrow, and includes a historically problematic race-derived variable that this baseline does not use. A random split also ignores neighborhood structure. The result is educational, not suitable for lending, appraisal, or policy decisions.

## Next step

Fit a regularized multivariate model, compare it with a tree ensemble, and report residual error by price band and location-related features.
