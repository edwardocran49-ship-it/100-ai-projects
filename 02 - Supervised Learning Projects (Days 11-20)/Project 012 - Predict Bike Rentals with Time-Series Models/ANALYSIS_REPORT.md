# Analysis Report: Predict Bike Rentals with Time-Series Models

**Author:** Edward Ocran  
**Project:** 12  
**Run status:** Verified locally

## Question

How accurately can recent demand and calendar/weather features forecast hourly bike rentals?

## Data used

After creating 1-hour, 24-hour, and 168-hour lags, 17,211 Washington D.C. hourly observations remained. The last 20% of time was held out without shuffling.

## Method

A histogram gradient-boosting regressor used calendar fields, normalized weather measures, and the three demand lags.

## Results

| Measure | Result |
|---|---:|
| Modeled hours | 17,211 |
| Holdout MAE | 29.6857 rentals |

## What the result means

The forecast is off by about thirty rentals in an average hour. The lag features carry substantial short- and weekly-cycle information, but the error should be read against hour-specific demand because thirty rentals is minor at rush hour and large overnight.

## Limitations

The data covers one city and two years. A single cutoff does not show seasonal stability, and the current metric weights quiet and busy hours equally.

## Next step

Report MAE by hour and season, compare against seasonal-naive forecasts, and use rolling-origin evaluation.
