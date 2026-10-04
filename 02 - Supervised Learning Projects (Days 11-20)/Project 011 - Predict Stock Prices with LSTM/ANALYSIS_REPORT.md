# Analysis Report: Predict Stock Prices with LSTM

**Author:** Edward Ocran  
**Project:** 11  
**Run status:** Verified locally

## Question

Can recent price sequences provide a useful next-day AAPL baseline?

## Data used

The run used 1,255 adjusted daily AAPL closes covering roughly five years. Prices came from Yahoo Finance through `yfinance`; the final 20% of the sequence was kept as a chronological holdout.

## Method

Twenty-day windows pass through a compact LSTM gate encoder. A regularized linear output layer maps the final hidden state to the next adjusted close.

## Results

| Measure | Result |
|---|---:|
| Trading days | 1,255 |
| Holdout MAE | $4.7309 |

## What the result means

The average absolute miss is about $4.73 per share over the holdout period. That is interpretable, but it needs comparison with a naive 'tomorrow equals today' forecast before claiming the sequence model adds value.

## Limitations

A single ticker and one market regime are not enough to establish robustness. The model ignores volume, corporate events, macro conditions, and transaction costs; it is not trading advice.

## Next step

Add naive and moving-average baselines, walk-forward retraining, directional accuracy, and error by volatility regime.
