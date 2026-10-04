# Analysis Report: Flight Delay Predictor

**Author:** Edward Ocran  
**Project:** 17  
**Run status:** Verified locally

## Question

Can schedule, route, and carrier information flag flights arriving more than fifteen minutes late?

## Data used

The run sampled the first 75,000 rows of the 2015 U.S. DOT file and retained 73,111 non-cancelled flights with arrival outcomes.

## Method

Numeric schedule fields and one-hot encoded carrier/airport fields fed a histogram gradient-boosting classifier. The split was stratified by delay status.

## Results

| Measure | Result |
|---|---:|
| Flights modeled | 73,111 |
| Accuracy | 75.34% |
| Delayed-flight F1 | 58.69% |

## What the result means

The overall score is respectable, but the delayed-flight F1 of 0.59 shows that the harder operational cases remain easy to miss. Accuracy alone would overstate performance because on-time flights are more common.

## Limitations

Using the first rows of the year creates a winter-heavy sample. A random split can also leak route and date patterns across train and test, and pre-departure weather is absent.

## Next step

Sample across the full year, use a chronological split, add weather, and tune the threshold for delay recall and alert cost.
