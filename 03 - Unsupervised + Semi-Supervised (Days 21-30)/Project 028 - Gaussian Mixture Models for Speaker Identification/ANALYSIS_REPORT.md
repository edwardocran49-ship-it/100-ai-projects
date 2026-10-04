# Gaussian Mixture Models for Speaker Identification — Analysis Report

**Author:** Edward Ocran  
**Project:** 28  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The eight-component GMM identifies speakers at 86.11% accuracy across 24 speakers—more than twenty times the 4.17% random baseline.
- Replacing generic spectral bands with the PDF-specified 13 MFCC coefficients produces a major improvement. The remaining errors likely reflect emotional delivery, intensity, and utterance variation within the RAVDESS recordings.
- **Recommended action:** Use this as an interpretable baseline and add MFCCs plus speaker-balanced validation.

## Analytical Question

Can MFCC-based Gaussian mixture models identify 24 speakers from held-out speech clips?

## Data and Evaluation Design

The analysis uses all 1,440 RAVDESS speech clips from 24 speakers. Each recording is converted to 13 MFCC coefficients, matching the PDF feature specification. One eight-component diagonal-covariance Gaussian mixture model is trained per speaker; every fifth clip is reserved for testing.

## Results

| Measure | Result |
|---|---:|
| Audio clips | 1,440 |
| Speakers | 24 |
| MFCC coefficients | 13 |
| Holdout accuracy | 86.11% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

![Benchmark and analytical context](analysis/context.png)

## What the Evidence Says

Replacing generic spectral bands with the PDF-specified 13 MFCC coefficients produces a major improvement. The remaining errors likely reflect emotional delivery, intensity, and utterance variation within the RAVDESS recordings.

## Risks and Limitations

The split is deterministic rather than session-based, and the dataset uses controlled recordings. Microphone, room, language, and background-noise shifts remain untested.

## Recommendations

1. Use this as an interpretable baseline and add MFCCs plus speaker-balanced validation.
2. Evaluate speaker-balanced cross-validation and robustness under added noise and channel changes.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
