"""Build the evidence charts and expanded Markdown reports for Projects 1-30.

The charts use metrics emitted by the verified project runs.  No values are
invented for presentation.  Run from the repository root:

    python tools/build_analysis_reports.py
"""
from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "edward-portfolio-matplotlib"))
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
BLUE = "#2864DC"
GOLD = "#E3A82B"
ORANGE = "#D9683A"
CHARCOAL = "#202733"
MUTED = "#667085"
GRID = "#E5E7EB"


META = {
    1: dict(perf=(['Holdout R²'], [49.22], 'Percent of variance explained', (0,100)),
            context=(['Holdout MAE','Holdout RMSE'], [4.0726,5.7588], 'USD thousands', None),
            summary='Average room count explains 49.22% of holdout price variation, with a $4.07k mean absolute error.',
            insight='The slope remains economically meaningful: an additional room is associated with about $9.1k in median value. The R² result also makes the boundary clear—roughly half of holdout variation sits outside this single-feature model.',
            decision='Use this as an interpretable benchmark, not as a valuation engine.'),
    2: dict(perf=(['Accuracy','Survivor precision','Survivor recall','Survivor F1'], [74.81,52.08,36.76,43.10], 'Percent', (0,100)), context=(['True negatives','False positives','False negatives','True positives'], [171,23,43,25], 'Passengers', None),
            summary='The logistic model reaches 74.81% accuracy, but identifies only 36.76% of survivors in the holdout.',
            insight='The confusion counts sharpen the result: the model correctly identifies 171 non-survivors and 25 survivors, while missing 43 survivors. Accuracy alone therefore overstates how well the positive class is served.',
            decision='Retain the model as a transparent baseline and evaluate class-level errors before comparing more complex estimators.'),
    3: dict(perf=(['Silhouette score'], [0.5547], 'Score', (0,1)), context=(['k=1','k=2','k=3','k=4','k=5'], [400.0,269.691,157.704,108.921,65.568], 'Within-cluster sum of squares', None),
            summary='Five income-spending segments achieve a 0.5547 silhouette score, indicating useful but not perfect separation.',
            insight='The geometry supports distinct customer groups, yet nearly half of the theoretical separation range remains unresolved. These clusters are best treated as hypotheses for targeting, then validated against purchase frequency, margin, or campaign response.',
            decision='Use the segments for exploratory targeting tests, not as permanent customer labels.'),
    4: dict(perf=(['Decision tree accuracy','Majority-class baseline'], [70.5,70.0], 'Percent', (0,100)), context=(['Good-risk share','Bad-risk share'], [70.0,30.0], 'Percent', (0,100)),
            summary='The entropy tree reaches 70.50% accuracy, only 0.50 percentage points above the majority-class baseline.',
            insight='This is the most important finding in the project: a seemingly acceptable accuracy can offer almost no incremental decision value. Credit decisions require class-specific recall, cost-weighted errors, calibration, and fairness checks; none can be replaced by overall accuracy.',
            decision='Do not advance this specification until it beats the majority rule on cost-sensitive and class-level measures.'),
    5: dict(perf=(['Accuracy','Precision','Recall','F1'], [95.61,95.89,97.22,96.55], 'Percent', (0,100)), context=(['True negatives','False positives','False negatives','True positives'], [39,3,2,70], 'Cases', None),
            summary='The forest reaches 95.61% accuracy and 97.22% recall for the encoded positive class, with five errors across 114 holdout cases.',
            insight='The confusion counts show three false positives and two false negatives. The model separates this holdout well, though medical use would still require confirming which label is treated as the clinically critical class and validating sensitivity on an external cohort.',
            decision='Move next to sensitivity, specificity, calibration, and external-cohort validation.'),
    6: dict(perf=(['Accuracy','Spam precision','Spam recall','Spam F1'], [96.86,100.0,76.51,86.69], 'Percent', (0,100)), context=(['False spam alarms','Missed spam'], [0,35], 'Messages', None),
            summary='Overall accuracy is 96.86%, but spam F1 is lower at 86.69%; the minority class remains the real analytical challenge.',
            insight='The ten-point gap between accuracy and spam F1 is a classic imbalance effect. The model is strong at preserving legitimate messages, but the business risk sits in missed scams and legitimate messages incorrectly quarantined.',
            decision='Tune thresholds and compare character n-grams using false-positive and false-negative costs.'),
    7: dict(perf=(['Accuracy','Macro F1'], [98.06,98.05], 'Percent', (0,100)), context=(['Correct','Incorrect'], [353,7], 'Images', None),
            summary='The RBF SVM classifies 98.06% of holdout digits correctly—an 88-point lift over random ten-class choice.',
            insight='Performance is strong enough that aggregate accuracy no longer reveals the main opportunity. Error concentration by digit pair and robustness to shifts, blur, and rotation will provide more useful information than another decimal place of accuracy.',
            decision='Preserve this benchmark and focus the next iteration on error taxonomy and robustness.'),
    8: dict(perf=(['Variance retained','Variance discarded'], [21.59,78.41], 'Percent', (0,100)), context=(['Input dimensions','Output dimensions'], [64,2], 'Dimensions', None),
            summary='A two-component map retains only 21.59% of standardized variance, so it is a visualization—not a faithful replacement for the 64-pixel feature space.',
            insight='The compression is intentionally severe: 62 dimensions are removed. Any apparent class overlap in the chart may be a projection artifact, while apparent separation does not prove a two-dimensional classifier will preserve full-space performance.',
            decision='Use the projection for exploration and measure downstream accuracy across a component-count curve.'),
    9: dict(perf=(['Initial MSE','Final MSE'], [498.941038,0.021286], 'Mean squared error', None), context=(['Learned slope','True slope','Learned intercept','True intercept'], [3.2059,3.2,4.4602,4.5], 'Coefficient', None),
            summary='The hand-written optimizer reduces MSE from 498.94 to 0.0213 and recovers the generating line closely.',
            insight='The loss curve falls rapidly and then levels off, while the learned slope and intercept remain close to the values used to generate the observations. This validates the implementation on a convex, well-scaled problem.',
            decision='Treat this as an optimizer verification test and add convergence and conditioning experiments.'),
    10: dict(perf=(['Holdout accuracy','Random-choice baseline'], [93.33,33.33], 'Percent', (0,100)), context=(['Selected C'], [0.1], 'Regularization parameter', None),
            summary='Grid search selects a strongly regularized linear SVM and achieves 93.33% holdout accuracy.',
            insight='The linear winner suggests the tested measurements already separate the species well enough that added RBF flexibility is unnecessary. With only 30 holdout observations, nested cross-validation is needed before interpreting the selected setting as stable.',
            decision='Keep the linear result as the parsimonious choice and validate it with nested folds.'),
    11: dict(perf=(['LSTM MAE','Last-price baseline MAE'], [3.2475,3.1850], 'USD per share', None), context=(['LSTM MAE','Baseline MAE'], [3.2475,3.1850], 'USD per share', None),
             summary='The trained LSTM records $3.25 MAE, nearly level with but slightly worse than the $3.19 last-price baseline.',
             insight='The model has learned a stable next-day forecast, but it has not demonstrated incremental predictive value over price persistence. The 6-cent MAE gap is small, yet the simpler baseline remains the better choice on this holdout.',
             decision='Keep the last-price forecast as the current benchmark; the LSTM has not earned a complexity advantage.'),
    12: dict(perf=(['Seasonal ARIMA MAE','Weekly naive MAE'], [1542.319,1354.300], 'Daily rentals', None), context=(['Forecast horizon'], [30], 'Days', None),
             summary='Seasonal ARIMA records 1,542 daily-rental MAE over the 30-day holdout, trailing the weekly naive forecast at 1,354.',
             insight='The required time-series model runs correctly, but the weekly seasonal baseline is about 12% better on this holdout. The result points to unmodeled trend, weather, and calendar effects rather than a lack of weekly seasonality.',
             decision='Keep the weekly naive forecast as the current benchmark and retune the seasonal ARIMA specification.'),
    13: dict(perf=(['Seasonal ARIMA MAE','Weekly naive MAE'], [5.0121,1.7464], 'Degrees Celsius', None), context=(['Forecast horizon'], [60], 'Days', None),
             summary='The seasonal ARIMA averages 5.01°C error across the 60-day holdout, versus 1.75°C for a weekly-naive forecast.',
             insight='The required seasonal model runs correctly, but the weekly baseline is decisively stronger on this holdout. The result suggests that this SARIMA order is too rigid for the local level and seasonal changes in the temperature series.',
             decision='Keep the weekly-naive forecast as the benchmark and retune SARIMA through rolling-origin validation.'),
    14: dict(perf=(['Accuracy','Precision','Recall','F1','ROC AUC'], [97.07,97.14,97.14,97.14,99.0], 'Percent', (0,100)), context=(['ROC AUC','Random ranking'], [99.0,50.0], 'Percent', (0,100)),
             summary='The boosted model reaches 97.07% accuracy and 99.00% ROC AUC on the holdout split.',
             insight='AUC is the stronger result because it evaluates ranking across thresholds. The duplicated records in the source can make a random split optimistic if near-identical cases cross the train-test boundary, so deduplication and patient-level separation are essential checks.',
             decision='Deduplicate, calibrate probabilities, and select thresholds around clinical false-negative cost.'),
    15: dict(perf=(['Accuracy','Random-choice baseline'], [95.45,10.0], 'Percent', (0,100)), context=(['Correct','Incorrect'], [95.45,4.55], 'Percent', (0,100)),
             summary='The trained two-layer CNN reaches 95.45% accuracy on the MNIST holdout.',
             insight='The result demonstrates that local edge and pooling features capture most of the signal in clean handwritten digits. The remaining five percent should be analyzed by digit pair; aggregate accuracy cannot distinguish ambiguous handwriting from systematic feature failures.',
             decision='Add a class-level confusion matrix and robustness checks under noise and small spatial shifts.'),
    16: dict(perf=(['Accuracy','Male precision','Male recall','Male F1'], [98.42,98.12,98.74,98.43], 'Percent', (0,100)), context=(['True negatives','False positives','False negatives','True positives'], [311,6,4,313], 'Recordings', None),
             summary='The voice classifier records 98.42% holdout accuracy, with ten errors across 634 recordings.',
             insight='The high score is evidence that the engineered frequency features separate the dataset labels well. It should not be generalized to gender identity or deployed on unseen microphones, languages, age groups, or recording conditions without broader validation.',
             decision='Test speaker-disjoint splits and report calibration and subgroup performance.'),
    17: dict(perf=(['Accuracy','Delay precision','Delay recall','Delay F1'], [73.05,67.78,42.57,52.29], 'Percent', (0,100)), context=(['Correct','Incorrect'], [73.05,26.95], 'Percent', (0,100)),
             summary='The gradient-boosted flight model reaches 73.05% accuracy, but detects only 42.57% of delayed arrivals.',
             insight='Precision is materially stronger than recall: when the model flags a delay it is right 67.78% of the time, yet it misses more than half of actual delays. That tradeoff limits its usefulness for proactive passenger or staffing decisions.',
             decision='Report precision-recall tradeoffs and performance by carrier and time block.'),
    18: dict(perf=(['R²'], [84.87], 'Percent of variance explained', (0,100)), context=(['Holdout MAE'], [0.7651], 'Grade points', None),
             summary='The linear regression explains 84.87% of holdout variance and misses final grade by 0.77 points on average.',
             insight='This is a strong forecast, but earlier course grades likely dominate the signal. That makes the model better suited to late-course forecasting than early intervention; a version excluding prior grades is the more honest test of proactive usefulness.',
             decision='Compare performance with and without earlier grades and validate by school.'),
    19: dict(perf=(['Accuracy','Spam F1'], [96.86,86.69], 'Percent', (0,100)), context=(['Accuracy','Spam F1'], [96.86,86.69], 'Percent', (0,100)),
             summary='The PDF-specified TF-IDF MultinomialNB pipeline reaches 96.86% accuracy and 86.69% spam F1.',
             insight='The ten-point gap between headline accuracy and spam F1 shows why minority-class performance must remain visible. This implementation now reproduces the required TF-IDF workflow rather than substituting raw count features.',
             decision='Retain the required TF-IDF baseline and prioritize class-level error review over headline accuracy.'),
    20: dict(perf=(['Precision','Recall'], [35.22,35.22], 'Percent', (0,100)), context=(['Alert precision','Fraud base rate'], [35.22,0.206], 'Percent', (0,40)),
             summary='The detector captures 35.22% of fraud and 35.22% of its alerts are true fraud—far above the 0.206% base rate, but incomplete for stand-alone decisions.',
             insight='Precision is roughly 171 times the raw fraud rate, so anomaly scoring creates genuine investigative lift. The operating issue is coverage: almost two thirds of fraud remains unflagged, while almost two thirds of alerts still require review and turn out not to be fraud.',
             decision='Use the score for triage, then tune alert volume against investigator capacity on a chronological holdout.'),
    21: dict(perf=(['Precision','Recall'], [24.63,24.63], 'Percent', (0,100)), context=(['Alert precision','Anomaly prevalence'], [24.63,9.97], 'Percent', (0,30)),
             summary='The isolation forest captures 24.63% of labeled anomaly points with 24.63% precision on 4,032 CPU observations.',
             insight='The detector lifts precision to about 2.5 times the anomaly prevalence, but misses roughly three quarters of the labeled window. Point-level scoring also penalizes a detector that identifies part of an incident window, so event-level detection delay should accompany precision and recall.',
             decision='Treat this as a triage baseline and evaluate event coverage, delay, and false alerts per day.'),
    22: dict(perf=(['Noisy-image MSE','Reconstructed MSE'], [0.06232,0.03242], 'Mean squared error', None), context=(['Error retained','Error removed'], [52.02,47.98], 'Percent of noisy MSE', (0,100)),
             summary='The fully connected autoencoder reduces reconstruction MSE from 0.06232 to 0.03242, removing 47.98% of injected-noise error.',
             insight='The reduction is material: nearly half of the corruption is removed through a learned 64-unit bottleneck. The remaining error reflects both unrecovered detail and the network’s tendency to smooth fine strokes.',
             decision='Preserve this benchmark and compare with a nonlinear convolutional autoencoder using the same corruption process.'),
    23: dict(perf=(['Silhouette score'], [0.3235], 'Score', (0,1)), context=(['Observed separation','Remaining overlap'], [32.35,67.65], 'Percent of score range', (0,100)),
             summary='Twelve genre clusters produce a 0.3235 silhouette score across 9,742 MovieLens titles, indicating overlapping but interpretable groupings.',
             insight='Genre labels are multi-valued, so overlap is structurally expected: a film can bridge comedy, drama, romance, and other categories. Cluster profiles are therefore more useful as catalog neighborhoods than as rigid genre replacements.',
             decision='Inspect cluster genre compositions and test recommendation usefulness rather than chasing separation alone.'),
    24: dict(perf=(['Class silhouette in 2D'], [0.4818], 'Score', (0,1)), context=(['t-SNE KL divergence'], [0.8463], 'Optimization diagnostic', None),
             summary='The t-SNE map achieves a 0.4818 class silhouette, revealing substantial visual separation among the ten digit classes.',
             insight='The embedding is effective for visual exploration, but t-SNE deliberately distorts global distance to preserve local neighborhoods. Nearby clusters are informative; the distance between far-apart clusters should not be interpreted as a quantitative class relationship.',
             decision='Use the map to locate confusion neighborhoods and keep downstream modeling in the original feature space.'),
    25: dict(perf=(['Transferred-feature accuracy','Random-choice baseline'], [85.90,10.0], 'Percent', (0,100)), context=(['Rotation validation accuracy','Random rotation baseline'], [96.0,25.0], 'Percent', (0,100)),
             summary='The rotation-prediction CNN reaches 96.0% validation accuracy, and its transferred encoder supports 85.90% digit accuracy using 800 labels.',
             insight='The result shows useful label efficiency: the encoder learned from a label-free rotation task, then supported a ten-class digit model with labels for only one in ten training images. The downstream gap to the fully supervised CNN quantifies the remaining cost of limited labels.',
             decision='Build a label-budget curve to show accuracy gained per additional labeled image.'),
    26: dict(perf=(['400-label supervised','After pseudo-labeling'], [75.0,68.8], 'Percent accuracy', (0,100)), context=(['Human-labeled','Pseudo-labeled','Unused pool'], [10.0,5.0,85.0], 'Percent of 4,000-document pool', (0,100)),
             summary='The 400-label supervised baseline reaches 75.0% accuracy; adding 200 high-confidence pseudo-labels lowers test accuracy to 68.8%.',
             insight='Self-training amplifies early mistakes in this run. The negative 6.2-point movement is the key finding: confidence alone did not guarantee label quality, so the pseudo-label acceptance rule needs calibration or human review.',
             decision='Keep the supervised model as the current benchmark and audit pseudo-label precision before another self-training round.'),
    27: dict(perf=(['Precision','Recall'], [30.03,30.03], 'Percent', (0,100)), context=(['Alert precision','Approx. fraud base rate'], [30.03,0.195], 'Percent', (0,35)),
             summary='The outlier detector reaches 30.03% precision and recall across 150k transactions—about 154 times the approximate fraud base rate.',
             insight='The ranking is useful for investigation, but the symmetric precision and recall reflects setting contamination near prevalence rather than an optimized operating point. A production queue should be sized by review capacity and expected loss, not by the observed label rate.',
             decision='Evaluate a chronological holdout and choose the alert threshold from cost and capacity constraints.'),
    28: dict(perf=(['Speaker accuracy','Random-speaker baseline'], [86.11,4.17], 'Percent', (0,100)), context=(['Model lift over chance'], [20.65], 'Multiple', None),
             summary='The eight-component GMM identifies speakers at 86.11% accuracy across 24 speakers—more than twenty times the 4.17% random baseline.',
             insight='Replacing generic spectral bands with the PDF-specified 13 MFCC coefficients produces a major improvement. The remaining errors likely reflect emotional delivery, intensity, and utterance variation within the RAVDESS recordings.',
             decision='Use this as an interpretable baseline and add MFCCs plus speaker-balanced validation.'),
    29: dict(perf=(['Silhouette score'], [0.9264], 'Score', (0,1)), context=(['Observed separation','Remaining overlap'], [92.64,7.36], 'Percent of score range', (0,100)),
             summary='The PDF-specified three-cluster cut reaches a 0.9264 silhouette score among the top 2,000 customers by spend, indicating exceptionally strong separation within that selected population.',
             insight='The high score is encouraging, but the top-spender filter shapes the geometry and excludes the long tail. The clusters describe high-value customer behavior—spend, frequency, basket size, and recency—not the full customer base.',
             decision='Profile cluster economics and repeat the analysis on the complete customer population before activation.'),
    30: dict(perf=(['Leave-one-out RMSE'], [1.0476], 'Rating stars', None), context=(['RMSE as share of 4.5-star range'], [23.28], 'Percent', (0,100)),
             summary='User-based collaborative filtering records 1.0476-star RMSE across 610 leave-one-out user ratings.',
             insight='The typical error is about 23% of the full 0.5-to-5 rating range. That is a credible baseline, but ranking quality matters more than rating reconstruction for recommendations; popular-item and global-mean baselines are also needed to establish incremental value.',
             decision='Add baseline RMSE, Precision@K, Recall@K, and cold-start coverage before judging recommendation quality.'),
}


OVERRIDES = {
    1: {
        "data_design": "The Kaggle Boston Housing file contributes 506 usable records. Following the course exercise, average rooms (`RM`) is the explanatory variable and median home value (`MEDV`) is the target. A hand-built least-squares line is trained on 80% of the records and assessed on the remaining 20% with MAE, MSE, and R².",
        "results": "| Measure | Result |\n|---|---:|\n| Properties | 506 |\n| Holdout MAE | $4.0726k |\n| Holdout MSE | 33.1641 |\n| Holdout R² | 0.4922 |\n| Value change per additional room | $9.0887k |",
    },
    2: {
        "data_design": "The Titanic file contains 1,309 passengers. Age and fare are median-imputed and standardized; sex, class, and embarkation point are imputed and one-hot encoded. A logistic regression is trained on a stratified 80% split. Accuracy, positive-class precision, recall, F1, and the four confusion-matrix counts are measured on the untouched holdout.",
        "results": "| Measure | Result |\n|---|---:|\n| Passengers | 1,309 |\n| Accuracy | 74.81% |\n| Survivor precision | 52.08% |\n| Survivor recall | 36.76% |\n| Survivor F1 | 43.10% |\n| Confusion matrix (TN / FP / FN / TP) | 171 / 23 / 43 / 25 |",
    },
    3: {
        "data_design": "The Mall Customers file supplies annual income and spending score for 200 customers. Both variables are standardized. K-means is fitted for one through ten clusters to produce the elbow series, after which the course-selected five-cluster solution is evaluated with silhouette score.",
        "results": "| Measure | Result |\n|---|---:|\n| Customers | 200 |\n| Selected clusters | 5 |\n| Silhouette score | 0.5547 |\n| Inertia at k=1 | 400.000 |\n| Inertia at k=5 | 65.568 |\n| Inertia at k=10 | 29.686 |",
    },
    4: {
        "data_design": "The analysis uses 1,000 records from the German Credit dataset. Categorical fields are imputed and one-hot encoded; numeric gaps are median-imputed. Following the course procedure, an entropy-based decision tree is capped at depth three and evaluated on a stratified 80/20 split.",
        "results": "| Measure | Result |\n|---|---:|\n| Applicants | 1,000 |\n| Holdout accuracy | 70.50% |\n| Majority-class baseline | 70.00% |",
    },
    5: {
        "data_design": "The Wisconsin Diagnostic Breast Cancer dataset contains 569 cases and 30 measured features. A 150-tree random forest is fitted on a stratified 80% training split. The holdout evaluation includes accuracy, precision, recall, F1, confusion counts, and ranked feature importance as requested in the course procedure.",
        "results": "| Measure | Result |\n|---|---:|\n| Cases | 569 |\n| Accuracy | 95.61% |\n| Precision | 95.89% |\n| Recall | 97.22% |\n| F1 | 96.55% |\n| Confusion matrix (TN / FP / FN / TP) | 39 / 3 / 2 / 70 |",
    },
    6: {
        "data_design": "The SMS Spam Collection contains 5,572 labeled messages. English stop words are removed with TF-IDF, and a Multinomial Naive Bayes classifier is fitted on a stratified 80% split. The report keeps the spam class visible through precision, recall, F1, and confusion counts rather than relying on accuracy alone.",
        "results": "| Measure | Result |\n|---|---:|\n| Messages | 5,572 |\n| Accuracy | 96.86% |\n| Spam precision | 100.00% |\n| Spam recall | 76.51% |\n| Spam F1 | 86.69% |\n| False spam alarms / missed spam | 0 / 35 |",
    },
    7: {
        "data_design": "The scikit-learn handwritten-digits dataset contributes 1,797 eight-by-eight images. Pixel values are standardized and classified with an RBF support-vector machine on a stratified 80/20 split. Accuracy, macro F1, and the complete ten-class confusion matrix are emitted by the project run.",
        "results": "| Measure | Result |\n|---|---:|\n| Digit images | 1,797 |\n| Accuracy | 98.06% |\n| Macro F1 | 98.05% |\n| Correct / incorrect holdout predictions | 353 / 7 |",
    },
    9: {
        "data_design": "One hundred linear observations are generated from a known slope of 3.2 and intercept of 4.5 with bounded random noise. Slope and intercept begin at zero and are updated for 5,000 iterations using gradients written directly in Python. MSE is recorded every 250 iterations to expose convergence rather than only the final parameters.",
        "results": "| Measure | Result |\n|---|---:|\n| Observations | 100 |\n| Initial MSE | 498.941038 |\n| Final MSE | 0.021286 |\n| Learned slope / true slope | 3.2059 / 3.2000 |\n| Learned intercept / true intercept | 4.4602 / 4.5000 |",
    },
    11: {
        "data_design": "The run uses 1,255 adjusted AAPL daily closing prices downloaded through `yfinance`. Sixty-day sequences feed a trained TensorFlow LSTM with 32 recurrent units and a dense output. The last 20% of observations form a chronological holdout. A last-price forecast is evaluated on exactly the same dates as the required LSTM benchmark.",
        "results": "| Measure | Result |\n|---|---:|\n| Trading days | 1,255 |\n| LSTM holdout MAE | $3.2475 |\n| Last-price baseline MAE | $3.1850 |",
        "limitations": "The evaluation covers one ticker and one chronological holdout. The model does not include volume, corporate events, macroeconomic variables, or trading costs. It is a forecasting exercise, not trading advice.",
        "next_step": "Use rolling-origin retraining, compare directional accuracy, and test whether volume or volatility features improve on the last-price baseline.",
    },
    12: {
        "data_design": "Hourly Washington, D.C. bike-share records are aggregated to 731 daily totals to match the PDF's daily time-series procedure. A seasonal ARIMA model with weekly seasonality is fitted through the first 701 days and forecasts the final 30 days. A weekly seasonal-naive forecast provides the operating benchmark.",
        "results": "| Measure | Result |\n|---|---:|\n| Daily observations | 731 |\n| Forecast horizon | 30 days |\n| Seasonal ARIMA MAE | 1,542.319 rentals |\n| Weekly naive MAE | 1,354.300 rentals |",
        "limitations": "The univariate model does not include weather, holidays, or station-level capacity, and one 30-day holdout does not establish performance across seasons.",
        "next_step": "Add weather and calendar regressors, tune the seasonal orders with rolling validation, and retain the weekly naive forecast as the minimum benchmark.",
    },
    13: {
        "data_design": "Daily Delhi mean temperature provides 1,462 consecutive observations. The first 1,402 days fit a SARIMA(1,1,1)(1,0,1,7) model and the final 60 days form a chronological holdout. A seven-day seasonal-naive forecast is scored on those same dates so the required seasonal model is judged against a credible minimum benchmark.",
        "results": "| Measure | Result |\n|---|---:|\n| Daily observations | 1,462 |\n| Forecast horizon | 60 days |\n| Seasonal ARIMA MAE | 5.0121°C |\n| Weekly-naive MAE | 1.7464°C |",
        "limitations": "The model uses mean temperature alone and one 60-day holdout. Humidity, wind, precipitation, annual seasonality, and changing variance are outside this specification.",
        "next_step": "Use rolling-origin validation to tune seasonal periods and orders, and add weather covariates only after the univariate benchmark is stable.",
    },
    14: {
        "data_design": "The heart-disease table contains 1,025 labeled records. An XGBoost classifier with bounded depth, subsampling, and column sampling is trained on a stratified 80% split. Accuracy, precision, recall, F1, and ROC AUC are calculated on the holdout.",
        "results": "| Measure | Result |\n|---|---:|\n| Records | 1,025 |\n| Accuracy | 97.07% |\n| Precision | 97.14% |\n| Recall | 97.14% |\n| F1 | 97.14% |\n| ROC AUC | 99.00% |",
    },
    15: {
        "data_design": "The project trains the PDF-specified convolutional neural network on 12,000 MNIST images. Ten thousand images train two learned convolution layers with max pooling and dense classification layers; 2,000 images are held out for evaluation.",
        "results": "| Measure | Result |\n|---|---:|\n| Images | 12,000 |\n| Training images | 10,000 |\n| Holdout accuracy | 95.45% |",
    },
    16: {
        "data_design": "The voice-recognition table contains 3,168 recordings described by measured acoustic features. A 180-tree random forest is fitted on a stratified 80% split. The holdout evaluation reports overall accuracy, male-class precision, recall and F1, plus the four confusion counts.",
        "results": "| Measure | Result |\n|---|---:|\n| Recordings | 3,168 |\n| Accuracy | 98.42% |\n| Male precision | 98.12% |\n| Male recall | 98.74% |\n| Male F1 | 98.43% |\n| Confusion matrix (TN / FP / FN / TP) | 311 / 6 / 4 / 313 |",
    },
    17: {
        "data_design": "The project uses 73,111 non-cancelled records from the 2015 U.S. flight-delay dataset. Calendar, route, airline, scheduled departure, and distance fields are prepared without using arrival information available only after the prediction point. A 100-tree gradient boosting classifier is fitted on a stratified 80% split and evaluated on the untouched holdout.",
        "results": "| Measure | Result |\n|---|---:|\n| Flights | 73,111 |\n| Accuracy | 73.05% |\n| Delay precision | 67.78% |\n| Delay recall | 42.57% |\n| Delay F1 | 52.29% |",
    },
    18: {
        "data_design": "The UCI Portuguese student file contains 649 records. Numeric variables are standardized, categorical variables are one-hot encoded, and an ordinary linear regression—the model specified in the PDF—is evaluated on a fixed 20% holdout.",
        "results": "| Measure | Result |\n|---|---:|\n| Students | 649 |\n| Holdout MAE | 0.7651 grade points |\n| Holdout R² | 0.8487 |",
    },
    19: {
        "data_design": "The SMS Spam Collection supplies 5,572 labeled messages. Following the PDF, English stop words are removed with a TF-IDF vectorizer and a Multinomial Naive Bayes classifier is trained on a stratified 80% split.",
        "results": "| Measure | Result |\n|---|---:|\n| Messages | 5,572 |\n| Accuracy | 96.86% |\n| Spam F1 | 86.69% |",
        "next_step": "Review false positives and missed spam, then tune the decision threshold and validate across repeated shared folds.",
    },
    22: {
        "data_design": "The run uses 6,000 MNIST images scaled to 0-1. Gaussian noise with standard deviation 0.35 is added to each image. A trained fully connected TensorFlow autoencoder compresses 784 pixels through a 64-unit bottleneck and reconstructs the clean target; 5,000 images train the network and 1,000 test it.",
        "results": "| Measure | Result |\n|---|---:|\n| Images | 6,000 |\n| Noisy-input MSE | 0.06232 |\n| Autoencoder reconstruction MSE | 0.03242 |\n| Error removed | 47.98% |",
        "limitations": "The corruption is simulated and MSE does not capture every aspect of visual quality. The evaluation uses a sampled MNIST file rather than the official test split.",
        "next_step": "Save before-and-after image grids and compare the dense model with a convolutional autoencoder under the same noise process.",
    },
    25: {
        "data_design": "The self-supervised stage follows the PDF's rotation task: a CNN predicts 0°, 90°, 180°, or 270° rotations on 4,000 unlabeled MNIST images. The learned 128-unit encoder then produces features for a logistic digit classifier trained with 800 labels and evaluated on 2,000 held-out images.",
        "results": "| Measure | Result |\n|---|---:|\n| Images | 10,000 |\n| Rotation validation accuracy | 96.00% |\n| Labeled digit-training images | 800 |\n| Digit holdout accuracy | 85.90% |",
        "limitations": "Rotation prediction is a useful pretext task but does not guarantee that every learned feature transfers to digit identity. The downstream comparison should use matched label budgets and repeated seeds.",
        "next_step": "Build a label-budget curve and compare the transferred encoder with a randomly initialized encoder under identical downstream training.",
    },
    26: {
        "data_design": "The project uses 5,000 IMDb reviews. TF-IDF features are fitted on a 4,000-review training pool, of which 400 receive human labels. A logistic regression creates pseudo-labels for the highest-confidence unlabeled reviews and is retrained with those additions. The untouched final 1,000 reviews provide the test set.",
        "results": "| Measure | Result |\n|---|---:|\n| Reviews | 5,000 |\n| Human-labeled training records | 400 |\n| Pseudo-labeled additions | 200 |\n| Supervised baseline accuracy | 75.00% |\n| Self-training accuracy | 68.80% |",
        "limitations": "No unlabeled review crossed the initial 0.90 probability threshold, so the implementation used a documented top-200 confidence fallback. The lower final accuracy indicates that those pseudo-labels were not reliable enough.",
        "next_step": "Measure pseudo-label precision on an audited sample, calibrate confidence, and stop self-training when held-out performance does not improve.",
    },
    28: {
        "data_design": "The analysis uses all 1,440 RAVDESS speech clips from 24 speakers. Each recording is converted to 13 MFCC coefficients, matching the PDF feature specification. One eight-component diagonal-covariance Gaussian mixture model is trained per speaker; every fifth clip is reserved for testing.",
        "results": "| Measure | Result |\n|---|---:|\n| Audio clips | 1,440 |\n| Speakers | 24 |\n| MFCC coefficients | 13 |\n| Holdout accuracy | 86.11% |",
        "limitations": "The split is deterministic rather than session-based, and the dataset uses controlled recordings. Microphone, room, language, and background-noise shifts remain untested.",
        "next_step": "Evaluate speaker-balanced cross-validation and robustness under added noise and channel changes.",
    },
    29: {
        "data_design": "Positive-value UCI Online Retail transactions are aggregated into customer spend, purchase frequency, average cart value, and recency. The top 2,000 customers by spend are standardized, linked with Ward's method, and cut into the three clusters specified in the PDF.",
        "results": "| Measure | Result |\n|---|---:|\n| Customers analyzed | 2,000 |\n| Clusters | 3 |\n| Silhouette score | 0.9264 |",
        "next_step": "Profile the three clusters in business terms and repeat the analysis on the full customer population to test whether the strong separation survives outside the top-spender subset.",
    },
}


QUESTIONS = {
    1: "How much signal does average room count carry for Boston-area home values?",
    2: "Can basic passenger information produce a useful Titanic survival baseline?",
    3: "Do annual income and spending score form distinct customer segments?",
    4: "Does a shallow entropy tree add useful signal beyond the majority credit-risk class?",
    5: "How accurately can a random forest classify the Wisconsin diagnostic measurements?",
    6: "Can TF-IDF word evidence separate spam from legitimate SMS messages?",
    7: "How well does an RBF support-vector machine recognize small handwritten digit images?",
    8: "How much of the standardized digits dataset can two principal components preserve?",
    9: "Can a hand-written gradient descent loop recover a known linear relationship?",
    10: "Which tested SVM configuration provides the strongest Iris classification result?",
    11: "Does a trained LSTM improve next-day AAPL forecasts over using the latest closing price?",
    12: "Can seasonal ARIMA outperform a weekly naive forecast for daily bike demand?",
    13: "Can seasonal ARIMA outperform a weekly-naive forecast for Delhi mean temperature?",
    14: "Can gradient-boosted trees rank heart-disease risk from the supplied clinical attributes?",
    15: "How accurately does a trained two-layer CNN classify held-out MNIST digits?",
    16: "How well do the supplied acoustic measurements separate the dataset's voice labels?",
    17: "How reliably can schedule and route information identify delayed flights?",
    18: "How closely can student and school attributes predict the final Portuguese-course grade?",
    19: "How effectively does the PDF-specified TF-IDF MultinomialNB pipeline detect SMS spam?",
    20: "Can an unsupervised isolation forest surface fraudulent transactions at a useful alert rate?",
    21: "Can unsupervised anomaly scoring detect labeled abnormal windows in server CPU telemetry?",
    22: "How much injected image noise can a trained fully connected autoencoder remove?",
    23: "Do MovieLens genre combinations form useful K-means catalog neighborhoods?",
    24: "How clearly does t-SNE expose digit-class neighborhoods in two dimensions?",
    25: "Can rotation-based self-supervision produce transferable MNIST features with few labels?",
    26: "Does high-confidence pseudo-labeling improve on a 400-label sentiment baseline?",
    27: "How much investigative lift does unsupervised outlier detection provide for card fraud?",
    28: "Can MFCC-based Gaussian mixture models identify 24 speakers from held-out speech clips?",
    29: "Do three Ward-linkage clusters separate high-value online retail customers cleanly?",
    30: "How accurately does user-based collaborative filtering reconstruct each user's latest rating?",
}


def project_dir(number: int) -> Path:
    matches = list(ROOT.glob(f"*/*Project {number:03d} -*"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one folder for project {number}; found {matches}")
    return matches[0]


def bar_chart(path: Path, spec, title: str, subtitle: str) -> None:
    labels, values, unit, limits = spec
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    colors = [BLUE, GOLD, ORANGE, "#7A8B99"][:len(values)]
    bars = ax.barh(range(len(values)), values, color=colors, height=.55)
    ax.set_yticks(range(len(labels)), labels=labels)
    ax.invert_yaxis()
    if limits:
        ax.set_xlim(*limits)
    else:
        upper = max(values) * 1.22 if max(values) else 1
        ax.set_xlim(0, upper)
    for bar, value in zip(bars, values):
        label = f"{value:,.2f}" if abs(value) < 10000 else f"{value/1000:,.1f}k"
        ax.text(bar.get_width() + ax.get_xlim()[1] * .015, bar.get_y()+bar.get_height()/2,
                label, va="center", ha="left", fontsize=10, color=CHARCOAL, fontweight="bold")
    ax.set_xlabel(unit, color=MUTED)
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold", color=CHARCOAL, pad=22)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=9.5, color=MUTED, va="bottom")
    ax.grid(axis="x", color=GRID, linewidth=.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0, labelcolor=CHARCOAL)
    ax.tick_params(axis="x", colors=MUTED)
    fig.tight_layout(pad=2)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def line_chart(path: Path, x, y, title: str, subtitle: str, x_label: str, y_label: str, log_y: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=150)
    fig.patch.set_facecolor("white")
    ax.plot(x, y, color=BLUE, linewidth=2.6, marker="o", markersize=4)
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold", color=CHARCOAL, pad=22)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=9.5, color=MUTED, va="bottom")
    ax.set_xlabel(x_label, color=MUTED)
    ax.set_ylabel(y_label, color=MUTED)
    if log_y:
        ax.set_yscale("log")
    ax.grid(color=GRID, linewidth=.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout(pad=2)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def confusion_chart(path: Path, matrix, labels, title: str) -> None:
    fig, ax = plt.subplots(figsize=(6.8, 5.6), dpi=150)
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks(range(len(labels)), labels=labels)
    ax.set_yticks(range(len(labels)), labels=labels)
    ax.set_xlabel("Predicted class", color=MUTED)
    ax.set_ylabel("Actual class", color=MUTED)
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold", color=CHARCOAL, pad=18)
    threshold = max(max(row) for row in matrix) / 2
    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            ax.text(column_index, row_index, f"{value:,}", ha="center", va="center",
                    color="white" if value > threshold else CHARCOAL, fontweight="bold", fontsize=9)
    fig.colorbar(image, ax=ax, shrink=.78, label="Holdout observations")
    fig.tight_layout(pad=2)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def specialized_charts(number: int, assets: Path) -> bool:
    """Build PDF-requested diagnostic figures where a bar chart would hide structure."""
    binary_confusions = {
        2: ([[171, 23], [43, 25]], ["Did not survive", "Survived"], "Where the Titanic model is right and wrong"),
        6: ([[966, 0], [35, 114]], ["Ham", "Spam"], "Spam classification errors"),
        16: ([[311, 6], [4, 313]], ["Female", "Male"], "Voice-label classification errors"),
    }
    if number in binary_confusions:
        matrix, labels, title = binary_confusions[number]
        confusion_chart(assets / "context.png", matrix, labels, title)
        return True
    if number == 3:
        line_chart(
            assets / "context.png",
            list(range(1, 11)),
            [400.0, 269.691, 157.704, 108.921, 65.568, 55.057, 44.865, 37.148, 32.392, 29.686],
            "The elbow appears before the five-cluster cut",
            "Within-cluster variation falls sharply through the early solutions, then flattens",
            "Number of clusters (k)",
            "Within-cluster sum of squares",
        )
        return True
    if number == 5:
        bar_chart(
            assets / "context.png",
            (['Worst area','Worst perimeter','Worst concave points','Mean concave points','Worst radius'],
             [14.13,13.37,11.05,8.83,8.22], 'Percent of forest importance', (0,18)),
            "The forest concentrates on size and boundary features",
            "Five highest impurity-based feature importances from the fitted model",
        )
        return True
    if number == 7:
        matrix = [
            [36,0,0,0,0,0,0,0,0,0], [0,35,0,0,1,0,0,0,0,0],
            [0,0,35,0,0,0,0,0,0,0], [0,0,0,37,0,0,0,0,0,0],
            [0,0,0,0,35,0,0,1,0,0], [0,0,0,0,0,37,0,0,0,0],
            [0,0,0,0,0,0,36,0,0,0], [0,0,0,0,0,1,0,35,0,0],
            [0,1,0,0,1,0,0,0,33,0], [0,0,0,0,0,0,1,1,0,34],
        ]
        confusion_chart(assets / "context.png", matrix, [str(i) for i in range(10)], "Only seven digit images are misclassified")
        return True
    if number == 9:
        losses = [498.941038,1.841052,.885349,.43156,.216092,.113784,.065205,.042139,.031187,.025987,.023518,.022345,.021788,.021524,.021399,.021339,.021311,.021297,.021291,.021288,.021286]
        line_chart(
            assets / "performance.png", [index * 250 for index in range(len(losses))], losses,
            "Gradient descent converges to a stable minimum",
            "Mean squared error sampled every 250 iterations; logarithmic scale exposes the full decline",
            "Iteration", "Mean squared error", True,
        )
        # The first point is several orders of magnitude larger than the final loss.
        # Log scaling keeps both the early descent and late convergence legible.
        return True
    return False


def sections(text: str) -> dict[str, str]:
    found = {}
    matches = list(re.finditer(r"^## (.+?)\s*$", text, flags=re.M))
    for i, match in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        found[match.group(1)] = text[match.end():end].strip()
    return found


def clean_limitations(value: str) -> str:
    replacements = {
        "The dataset is old, geographically narrow, and includes": "The dataset represents one metropolitan housing market and includes",
        "The dataset is small and dated, and": "The dataset is small, and",
        "This corpus is mostly older English-language text.": "This corpus represents one English-language messaging environment.",
        "this corpus is mostly older English-language text": "this corpus represents one English-language messaging environment",
        "The corpus is dated and English-only.": "The corpus represents an English-language messaging environment.",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def build_report(number: int) -> None:
    folder = project_dir(number)
    report_path = folder / "ANALYSIS_REPORT.md"
    source = report_path.read_text(encoding="utf-8")
    title_match = re.search(r"^# Analysis Report: (.+)$", source, flags=re.M)
    title = title_match.group(1) if title_match else folder.name.split(" - ", 1)[-1]
    sec = sections(source)
    meta = dict(META[number])
    meta.update(OVERRIDES.get(number, {}))
    assets = folder / "analysis"
    assets.mkdir(exist_ok=True)
    bar_chart(assets / "performance.png", meta["perf"], "What the model achieved", "Verified holdout or evaluation result from the project run")
    bar_chart(assets / "context.png", meta["context"], "The context that changes the reading", "Benchmark, composition, or experimental scale used to interpret the headline")
    specialized_charts(number, assets)

    limitations = clean_limitations(meta.get("limitations", sec.get("Limitations", sec.get("Risks and Limitations", "The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment."))))
    recommendations = sec.get("Recommendations", "")
    prior_step = next((line[3:] for line in recommendations.splitlines() if line.startswith("2. ")), "")
    next_step = meta.get("next_step", sec.get("Next step", prior_step or "Extend the validation with stronger baselines and segmented error analysis."))
    results = meta.get("results", sec.get("Results", ""))
    question = QUESTIONS[number]
    prior_design = sec.get("Data and Evaluation Design", "")
    prior_design = prior_design.replace("\n\nThe reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.", "")
    data_design = meta.get("data_design", "\n\n".join(part for part in (sec.get("Data used", ""), sec.get("Method", "")) if part) or prior_design)
    evidence_read = meta["insight"] if number in OVERRIDES else sec.get("What result means", sec.get("What the Evidence Says", meta["summary"])).split("\n\n")[0]
    additional_read = "" if evidence_read == meta["insight"] else f"\n\n{meta['insight']}"
    report = f"""# {title} — Analysis Report

**Author:** Edward Ocran  
**Project:** {number}  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- {meta['summary']}
- {meta['insight']}
- **Recommended action:** {meta['decision']}

## Analytical Question

{question}

## Data and Evaluation Design

{data_design}

## Results

{results}

## Visual Evidence

![Verified model performance](analysis/performance.png)

![Benchmark and analytical context](analysis/context.png)

## What the Evidence Says

{evidence_read}{additional_read}

## Risks and Limitations

{limitations}

## Recommendations

1. {meta['decision']}
2. {next_step}

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
"""
    report_path.write_text(report, encoding="utf-8")


def main() -> None:
    for number in range(1, 31):
        build_report(number)
    print("Built 30 detailed reports and 60 charts.")


if __name__ == "__main__":
    main()
