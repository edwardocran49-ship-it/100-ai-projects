# Analysis Report: Student Grade Predictor with Linear Regression

**Author:** Edward Ocran  
**Project:** 18  
**Run status:** Verified locally

## Question

How closely can demographic, school, and earlier-grade information predict the final Portuguese-course grade?

## Data used

The UCI-derived file contains 649 students. Numeric variables were standardized and categorical variables one-hot encoded.

## Method

Ridge regression was trained on 80% of the records and assessed with MAE and R².

## Results

| Measure | Result |
|---|---:|
| Students | 649 |
| MAE | 0.7612 grade points |
| R² | 0.8494 |

## What the result means

The model explains about 85% of holdout variance and misses by less than one grade point on average. Earlier period grades are likely doing much of that work, so this is closer to late-course forecasting than early intervention.

## Limitations

Students come from only two schools, records are limited, and a random split does not test transfer to a new school or year. Several attributes are sensitive and should not drive punitive decisions.

## Next step

Measure performance without G1/G2, validate by school, inspect residuals, and document a supportive—not disciplinary—use case.
