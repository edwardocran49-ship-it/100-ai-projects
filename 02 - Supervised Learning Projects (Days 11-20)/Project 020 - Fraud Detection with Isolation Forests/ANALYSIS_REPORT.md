# Analysis Report: Fraud Detection with Isolation Forests

**Author:** Edward Ocran  
**Project:** 20  
**Run status:** Verified locally

## Question

Can an unsupervised isolation forest surface fraudulent transactions without using labels for training?

## Data used

The run used the first 120,000 anonymized transactions, including 247 labeled frauds. Labels were reserved for evaluation; the detector fitted only the transaction features.

## Method

All features were standardized. Isolation Forest contamination was set to the observed fraud rate, and flagged anomalies were compared with the held-out labels in the same sample.

## Results

| Measure | Result |
|---|---:|
| Transactions | 120,000 |
| Fraud records | 247 |
| Precision | 35.22% |
| Recall | 35.22% |

## What the result means

The detector finds roughly one third of frauds, and only about one third of its alerts are true fraud. That is far better than random selection at the base rate, but still too noisy and incomplete for a stand-alone fraud decision system.

## Limitations

The contamination rate comes from labels, the sample is chronological rather than randomized, and evaluation occurs on the fitted observations. Costs, concept drift, and investigator capacity are not modeled.

## Next step

Use a chronological train/test split, tune alert volume by review capacity, and compare supervised models plus precision-recall curves.
