# Analysis Report: Forecast Weather Using ARIMA

**Author:** Edward Ocran  
**Project:** 13  
**Run status:** Verified locally

## Question

Can a compact ARIMA model forecast Delhi mean temperature two months ahead?

## Data used

The series contains 1,462 daily Delhi climate records. The final sixty days form a chronological holdout.

## Method

An ARIMA(5,1,1) model was fitted to mean temperature only and forecast the next sixty observations.

## Results

| Measure | Result |
|---|---:|
| Daily observations | 1,462 |
| Forecast horizon | 60 days |
| Holdout MAE | 4.8914 °C |

## What the result means

An average error near 4.9°C is too wide for a strong weather forecast. The model captures serial movement but misses seasonal and exogenous structure that matters over a two-month horizon.

## Limitations

The order was not tuned, seasonality is absent, and humidity, wind, and pressure are ignored. This is a time-series exercise, not an operational weather service.

## Next step

Compare seasonal ARIMA and Prophet-style models, add exogenous variables, and evaluate shorter horizons with rolling backtests.
