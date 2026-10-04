# Dataset Execution Audit

**Author:** Edward Ocran

**Audit date:** 2026-10-04

**Scope:** Every project that contains `DATASET.md`

## Conclusion

The portfolio contains **46 dataset-backed projects**. Each was executed through its normal entry point with `PORTFOLIO_FAST_VALIDATION` unset. All 46 completed successfully while loading the documented external, built-in, recorded, or course-generated dataset. The remaining 54 projects are application, service, hardware, document, media, simulation, or reflection projects and are documented with `INPUTS.md` instead.

The dataset files themselves are not all committed to Git. Large files and sources with redistribution constraints are retrieved through the project's `download_data.py`, `kagglehub`, a public API, or a library-provided loader. A GitHub smoke pass is separate from the full runs recorded here.

## Execution evidence

| Project | Dataset used by the normal path | Evidence returned by the run |
|---:|---|---|
| 001 | Boston Housing CSV | 506 records; regression metrics produced |
| 002 | Titanic passenger data | 1,309 records; classification metrics produced |
| 003 | Mall Customers | 200 records; five-cluster evaluation produced |
| 004 | German Credit Risk | 1,000 records; decision-tree metrics produced |
| 005 | Wisconsin Diagnostic Breast Cancer | 569 records; forest metrics and feature importances produced |
| 006 | SMS Spam Collection | 5,572 messages; spam classification metrics produced |
| 007 | scikit-learn handwritten digits | 1,797 images; SVM confusion matrix produced |
| 008 | scikit-learn handwritten digits | 1,797 images; PCA variance result produced |
| 009 | Course-defined generated linear observations | 100 observations; optimization loss history produced |
| 010 | Iris | 150 records; grid-search result produced |
| 011 | AAPL adjusted daily prices | 1,255 prices; TensorFlow LSTM and baseline MAE produced |
| 012 | Washington, D.C. bike sharing | 731 daily records; SARIMA and seasonal-baseline MAE produced |
| 013 | Daily Delhi Climate | 1,462 daily records; SARIMA evaluation produced |
| 014 | Heart Disease | 1,025 records; XGBoost classification metrics produced |
| 015 | MNIST | 12,000 images used by the run; CNN accuracy produced |
| 016 | Gender Recognition by Voice | 3,168 acoustic-feature rows; classification metrics produced |
| 017 | 2015 Flight Delays and Cancellations | 73,111 records used by the run; delay metrics produced |
| 018 | UCI Student Performance | 649 records; regression metrics produced |
| 019 | SMS Spam Collection | 5,572 messages; MultinomialNB metrics produced |
| 020 | Credit Card Fraud Detection | 120,000 transactions used by the run; anomaly metrics produced |
| 021 | Numenta Anomaly Benchmark EC2 CPU | 4,032 observations; anomaly evaluation produced |
| 022 | MNIST | 6,000 images used by the run; noisy and reconstructed MSE produced |
| 023 | MovieLens latest-small movies | 9,742 movies; clustering evaluation produced |
| 024 | scikit-learn handwritten digits | 1,797 images; t-SNE evaluation produced |
| 025 | MNIST | 10,000 images used by the run; pretext and transfer accuracy produced |
| 026 | IMDb 50K Movie Reviews | 5,000 reviews used by the run; supervised and self-training results produced |
| 027 | Credit Card Fraud Detection | 150,000 transactions used by the run; outlier metrics produced |
| 028 | RAVDESS | 1,440 recordings from 24 speakers; GMM accuracy produced |
| 029 | UCI Online Retail | 2,000 transaction records used by the run; hierarchical-clustering score produced |
| 030 | MovieLens latest-small ratings | 100,836 ratings from 610 users; recommender RMSE produced |
| 031 | IMDb 50K Movie Reviews | Balanced 200-review evaluation sample; DistilBERT confusion metrics produced |
| 034 | SMS Spam Collection | 5,572 messages; TF-IDF/MultinomialNB metrics produced |
| 047 | PlantVillage | 240 images used by the run across three classes; CNN metrics produced |
| 048 | FER-2013 | 560 images used by the run across seven classes; CNN metrics produced |
| 050 | DeepGlobe Land Cover | Six image-mask pairs used by the run; segmentation loss and mean IoU produced |
| 064 | UrbanSound8K | 300 genuine clips across ten classes; audio-classification confusion matrix produced |
| 067 | RAVDESS | 192 recordings across eight emotions; classification confusion matrix produced |
| 068 | Google Speech Commands v0.01 | 1,000 recordings across ten commands; confusion matrix produced |
| 072 | Kaggle Auto Insurance Claims | 1,000 claims; fraud classification metrics produced |
| 073 | NIH PubChem canonical structures | Eight compounds; Morgan-fingerprint similarity ranking produced |
| 074 | AAPL daily prices | 1,255 prices; ARIMA holdout and forecast interval produced |
| 075 | Kaggle Loan Prediction | 614 applications; classification and ROC-AUC metrics produced |
| 076 | UCI Online Retail | 374 daily aggregates derived from the source transactions; demand forecast produced |
| 077 | IBM Telco Customer Churn | 7,043 customers; churn classification and ROC-AUC metrics produced |
| 079 | UCI Sentiment Labelled Sentences, Amazon subset | 1,000 reviews; sentiment and aspect results produced |
| 096 | Official OpenBCI GUI EEG sample recordings | Two recordings segmented into 209 windows; BCI classification metrics produced |

## Corrections made during the audit

- Projects 61, 63, and 66 were reclassified from dataset-backed projects to input-driven speech utilities because they evaluate a supplied recording rather than train on a corpus.
- Project 78 was reclassified as input-driven because it processes a deterministic retail image fixture rather than a training dataset.
- Projects 67, 68, 73, 76, and 79 now resolve their downloaded local data automatically on a normal run while retaining explicit path overrides.
- TensorFlow projects were verified in Python 3.11 because TensorFlow is not available for the machine's default Python 3.14 runtime.

## Reproduction boundary

Run `python download_data.py` where supplied, install the project's requirements, and then run `python main.py --json`. Dataset projects that use `kagglehub` require network access and a working Kaggle session. Exact metrics can vary slightly across dependency versions and CPU kernels, but the source, record coverage, and execution path remain inspectable in each project.
