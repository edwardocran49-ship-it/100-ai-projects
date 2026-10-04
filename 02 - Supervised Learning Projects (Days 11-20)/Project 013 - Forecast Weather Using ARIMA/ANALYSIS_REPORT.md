# Forecast Weather Using ARIMA — Analysis Report

**Author:** Edward Ocran  
**Project:** 13  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The seasonal ARIMA averages 5.01°C error across the 60-day holdout, versus 1.75°C for a weekly-naive forecast.
- The required seasonal model runs correctly, but the weekly baseline is decisively stronger on this holdout. The result suggests that this SARIMA order is too rigid for the local level and seasonal changes in the temperature series.
- **Recommended action:** Keep the weekly-naive forecast as the benchmark and retune SARIMA through rolling-origin validation.

## Analytical Question

Can seasonal ARIMA outperform a weekly-naive forecast for Delhi mean temperature?

## Data and Evaluation Design

Daily Delhi mean temperature provides 1,462 consecutive observations. The first 1,402 days fit a SARIMA(1,1,1)(1,0,1,7) model and the final 60 days form a chronological holdout. A seven-day seasonal-naive forecast is scored on those same dates so the required seasonal model is judged against a credible minimum benchmark.

## Results

| Measure | Result |
|---|---:|
| Daily observations | 1,462 |
| Forecast horizon | 60 days |
| Seasonal ARIMA MAE | 5.0121°C |
| Weekly-naive MAE | 1.7464°C |

## Visual Evidence

![Verified model performance](analysis/performance.png)

![Benchmark and analytical context](analysis/context.png)

## What the Evidence Says

The required seasonal model runs correctly, but the weekly baseline is decisively stronger on this holdout. The result suggests that this SARIMA order is too rigid for the local level and seasonal changes in the temperature series.

## Risks and Limitations

The model uses mean temperature alone and one 60-day holdout. Humidity, wind, precipitation, annual seasonality, and changing variance are outside this specification.

## Recommendations

1. Keep the weekly-naive forecast as the benchmark and retune SARIMA through rolling-origin validation.
2. Use rolling-origin validation to tune seasonal periods and orders, and add weather covariates only after the univariate benchmark is stable.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- The committed figures correspond to the measured results documented in this report.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
