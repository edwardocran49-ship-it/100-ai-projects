# Predict Bike Rentals with Time-Series Models — Analysis Report

**Author:** Edward Ocran  
**Project:** 12  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- Seasonal ARIMA records 1,542 daily-rental MAE over the 30-day holdout, trailing the weekly naive forecast at 1,354.
- The required time-series model runs correctly, but the weekly seasonal baseline is about 12% better on this holdout. The result points to unmodeled trend, weather, and calendar effects rather than a lack of weekly seasonality.
- **Recommended action:** Keep the weekly naive forecast as the current benchmark and retune the seasonal ARIMA specification.

## Analytical Question

Can seasonal ARIMA outperform a weekly naive forecast for daily bike demand?

## Data and Evaluation Design

Hourly Washington, D.C. bike-share records are aggregated to 731 daily totals to match the PDF's daily time-series procedure. A seasonal ARIMA model with weekly seasonality is fitted through the first 701 days and forecasts the final 30 days. A weekly seasonal-naive forecast provides the operating benchmark.

## Results

| Measure | Result |
|---|---:|
| Daily observations | 731 |
| Forecast horizon | 30 days |
| Seasonal ARIMA MAE | 1,542.319 rentals |
| Weekly naive MAE | 1,354.300 rentals |

## Visual Evidence

![Verified model performance](analysis/performance.png)

![Benchmark and analytical context](analysis/context.png)

## What the Evidence Says

The required time-series model runs correctly, but the weekly seasonal baseline is about 12% better on this holdout. The result points to unmodeled trend, weather, and calendar effects rather than a lack of weekly seasonality.

## Risks and Limitations

The univariate model does not include weather, holidays, or station-level capacity, and one 30-day holdout does not establish performance across seasons.

## Recommendations

1. Keep the weekly naive forecast as the current benchmark and retune the seasonal ARIMA specification.
2. Add weather and calendar regressors, tune the seasonal orders with rolling validation, and retain the weekly naive forecast as the minimum benchmark.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- The committed figures correspond to the measured results documented in this report.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
