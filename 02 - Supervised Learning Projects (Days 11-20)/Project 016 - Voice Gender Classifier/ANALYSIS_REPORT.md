# Analysis Report: Voice Gender Classifier

**Author:** Edward Ocran  
**Project:** 16  
**Run status:** Verified locally

## Question

Can acoustic summary features classify the labeled voice samples?

## Data used

The source provides 3,168 voice samples represented by twenty acoustic measurements and a male/female label.

## Method

A 180-tree random forest was trained on a stratified 80% split.

## Results

| Measure | Result |
|---|---:|
| Samples | 3,168 |
| Holdout accuracy | 98.42% |

## What the result means

The holdout score is high, showing that the engineered frequency and spectral features strongly separate the two labels in this corpus. It does not establish that the same boundary works across languages, microphones, ages, or gender-diverse populations.

## Limitations

The labels are binary, the dataset is licensed for non-commercial share-alike use, and speaker-level leakage cannot be ruled out from the available table alone.

## Next step

Use speaker-disjoint validation, report subgroup error, and reframe the task around acoustic characteristics rather than inferring identity.
