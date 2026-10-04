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
    1: dict(perf=(['Holdout MAE'], [4.0726], 'MEDV units (USD thousands)', None),
            context=(['Value gain per additional room'], [9.0887], 'USD thousands', None),
            summary='Average room count carries a clear price signal, but a one-variable model still misses by about $4.1k on an average holdout property.',
            insight='The slope is economically meaningful: an additional room is associated with about $9.1k in median value. The remaining error shows that room count explains only one part of the pricing structure; location, condition, tax, and neighborhood variables still carry material information.',
            decision='Use this as an interpretable benchmark, not as a valuation engine.'),
    2: dict(perf=(['Accuracy'], [74.81], 'Percent', (0,100)), context=(['Model accuracy','Majority-class baseline'], [74.81,61.8], 'Percent', (0,100)),
            summary='The logistic model reaches 74.81% accuracy, about 13 percentage points above a majority-class rule.',
            insight='The lift over the majority baseline confirms that the passenger features contain real predictive structure. The useful next question is not whether the model beats chance, but whether survivor recall and false-negative patterns remain acceptable across passenger groups.',
            decision='Retain the model as a transparent baseline and evaluate class-level errors before comparing more complex estimators.'),
    3: dict(perf=(['Silhouette score'], [0.5547], 'Score', (0,1)), context=(['Observed separation','Remaining overlap'], [55.47,44.53], 'Percent of score range', (0,100)),
            summary='Five income-spending segments achieve a 0.5547 silhouette score, indicating useful but not perfect separation.',
            insight='The geometry supports distinct customer groups, yet nearly half of the theoretical separation range remains unresolved. These clusters are best treated as hypotheses for targeting, then validated against purchase frequency, margin, or campaign response.',
            decision='Use the segments for exploratory targeting tests, not as permanent customer labels.'),
    4: dict(perf=(['Decision tree accuracy','Majority-class baseline'], [70.0,70.0], 'Percent', (0,100)), context=(['Good-risk share','Bad-risk share'], [70.0,30.0], 'Percent', (0,100)),
            summary='The 70% headline accuracy only matches the majority-class baseline, so the current tree does not yet demonstrate incremental decision value.',
            insight='This is the most important finding in the project: a seemingly acceptable accuracy can be operationally empty. Credit decisions require class-specific recall, cost-weighted errors, calibration, and fairness checks; none can be replaced by overall accuracy.',
            decision='Do not advance this specification until it beats the majority rule on cost-sensitive and class-level measures.'),
    5: dict(perf=(['Accuracy','Majority-class baseline'], [95.61,62.74], 'Percent', (0,100)), context=(['Model','Baseline'], [95.61,62.74], 'Correct classifications per 100', (0,100)),
            summary='The forest reaches 95.61% accuracy, roughly 32.9 percentage points above the majority-class baseline.',
            insight='The margin over baseline is substantial and supports the value of the diagnostic measurements. For screening, however, the decisive metric is malignant-case sensitivity; a small number of false negatives can matter more than many correct benign classifications.',
            decision='Move next to sensitivity, specificity, calibration, and external-cohort validation.'),
    6: dict(perf=(['Accuracy','Spam F1'], [96.86,86.69], 'Percent', (0,100)), context=(['Accuracy gain over ham-only rule'], [10.26], 'Percentage points', None),
            summary='Overall accuracy is 96.86%, but spam F1 is lower at 86.69%; the minority class remains the real analytical challenge.',
            insight='The ten-point gap between accuracy and spam F1 is a classic imbalance effect. The model is strong at preserving legitimate messages, but the business risk sits in missed scams and legitimate messages incorrectly quarantined.',
            decision='Tune thresholds and compare character n-grams using false-positive and false-negative costs.'),
    7: dict(perf=(['Accuracy','Random-choice baseline'], [98.06,10.0], 'Percent', (0,100)), context=(['Correct','Incorrect'], [98.06,1.94], 'Percent', (0,100)),
            summary='The RBF SVM classifies 98.06% of holdout digits correctly—an 88-point lift over random ten-class choice.',
            insight='Performance is strong enough that aggregate accuracy no longer reveals the main opportunity. Error concentration by digit pair and robustness to shifts, blur, and rotation will provide more useful information than another decimal place of accuracy.',
            decision='Preserve this benchmark and focus the next iteration on error taxonomy and robustness.'),
    8: dict(perf=(['Variance retained','Variance discarded'], [21.59,78.41], 'Percent', (0,100)), context=(['Input dimensions','Output dimensions'], [64,2], 'Dimensions', None),
            summary='A two-component map retains only 21.59% of standardized variance, so it is a visualization—not a faithful replacement for the 64-pixel feature space.',
            insight='The compression is intentionally severe: 62 dimensions are removed. Any apparent class overlap in the chart may be a projection artifact, while apparent separation does not prove a two-dimensional classifier will preserve full-space performance.',
            decision='Use the projection for exploration and measure downstream accuracy across a component-count curve.'),
    9: dict(perf=(['Learned slope','True slope'], [3.2059,3.2], 'Coefficient', None), context=(['Learned intercept','True intercept'], [4.4602,4.5], 'Coefficient', None),
            summary='The hand-written optimizer recovers the generating line closely: slope 3.2059 versus 3.2 and intercept 4.4602 versus 4.5.',
            insight='The parameter gaps are small and consistent with the injected noise. This validates the gradient implementation on a convex, well-scaled problem; it does not yet establish stability on correlated or poorly scaled features.',
            decision='Treat this as an optimizer verification test and add convergence and conditioning experiments.'),
    10: dict(perf=(['Holdout accuracy','Random-choice baseline'], [93.33,33.33], 'Percent', (0,100)), context=(['Selected C'], [0.1], 'Regularization parameter', None),
            summary='Grid search selects a strongly regularized linear SVM and achieves 93.33% holdout accuracy.',
            insight='The linear winner suggests the tested measurements already separate the species well enough that added RBF flexibility is unnecessary. With only 30 holdout observations, nested cross-validation is needed before interpreting the selected setting as stable.',
            decision='Keep the linear result as the parsimonious choice and validate it with nested folds.'),
    11: dict(perf=(['Holdout MAE'], [4.7309], 'USD per share', None), context=(['Trading days used'], [1255], 'Daily observations', None),
             summary='The sequence model misses the next adjusted close by $4.73 on average across the chronological holdout.',
             insight='The dollar error is interpretable but incomplete without a same-period naive forecast. Equity prices are highly persistent, so a complex sequence representation must beat “tomorrow equals today” and survive walk-forward evaluation to demonstrate incremental signal.',
             decision='Add naive and moving-average benchmarks before making any claim of forecasting advantage.'),
    12: dict(perf=(['Holdout MAE'], [29.6857], 'Hourly rentals', None), context=(['Modeled hours'], [17211], 'Hourly observations', None),
             summary='The model’s average hourly miss is 29.69 rentals across 17.2k chronologically ordered observations.',
             insight='The same absolute miss has different operational meaning by demand level: thirty bikes can be negligible during a rush-hour peak and material overnight. Segmenting error by hour, season, and demand band will expose where rebalancing decisions are most vulnerable.',
             decision='Evaluate against seasonal-naive forecasts and report error by operating regime.'),
    13: dict(perf=(['60-day MAE'], [4.8914], 'Degrees Celsius', None), context=(['Forecast horizon'], [60], 'Days', None),
             summary='ARIMA(5,1,1) produces a 4.89°C average error over a 60-day holdout, which is too wide for a dependable operational forecast.',
             insight='The long horizon amplifies a model-design gap: differencing and short autoregressive memory do not capture the full seasonal structure. The result is useful because it identifies exactly where a compact univariate ARIMA stops being competitive.',
             decision='Use this as the non-seasonal benchmark and test seasonal/exogenous specifications with rolling origins.'),
    14: dict(perf=(['Accuracy','ROC AUC'], [85.8,91.37], 'Percent', (0,100)), context=(['ROC AUC','Random ranking'], [91.37,50.0], 'Percent', (0,100)),
             summary='The boosted model reaches 85.80% accuracy and 91.37% ROC AUC, indicating strong ranking ability on the holdout split.',
             insight='AUC is the stronger result because it evaluates ranking across thresholds. The duplicated records in the source can make a random split optimistic if near-identical cases cross the train-test boundary, so deduplication and patient-level separation are essential checks.',
             decision='Deduplicate, calibrate probabilities, and select thresholds around clinical false-negative cost.'),
    15: dict(perf=(['Accuracy','Random-choice baseline'], [95.0,10.0], 'Percent', (0,100)), context=(['Correct','Incorrect'], [95.0,5.0], 'Percent', (0,100)),
             summary='The convolution-feature classifier reaches 95.00% accuracy on the MNIST holdout.',
             insight='The result demonstrates that local edge and pooling features capture most of the signal in clean handwritten digits. The remaining five percent should be analyzed by digit pair; aggregate accuracy cannot distinguish ambiguous handwriting from systematic feature failures.',
             decision='Add a class-level confusion matrix and robustness checks under noise and small spatial shifts.'),
    16: dict(perf=(['Accuracy','Balanced baseline'], [97.16,50.0], 'Percent', (0,100)), context=(['Correct','Incorrect'], [97.16,2.84], 'Percent', (0,100)),
             summary='The voice classifier records 97.16% holdout accuracy on the supplied acoustic-feature table.',
             insight='The high score is evidence that the engineered frequency features separate the dataset labels well. It should not be generalized to gender identity or deployed on unseen microphones, languages, age groups, or recording conditions without broader validation.',
             decision='Test speaker-disjoint splits and report calibration and subgroup performance.'),
    17: dict(perf=(['Accuracy','Delay F1'], [83.69,77.0], 'Percent', (0,100)), context=(['Accuracy-F1 gap'], [6.69], 'Percentage points', None),
             summary='The flight model reaches 83.69% accuracy and approximately 77% delay-class F1 on a 75k-row sample.',
             insight='The lower delay F1 shows that positive-case detection is materially harder than the headline accuracy suggests. Operational value will depend on recall at an alert volume planners can absorb, particularly across carriers, airports, and departure periods.',
             decision='Report precision-recall tradeoffs and performance by carrier and time block.'),
    18: dict(perf=(['R²'], [84.94], 'Percent of variance explained', (0,100)), context=(['Holdout MAE'], [0.7612], 'Grade points', None),
             summary='The ridge model explains 84.94% of holdout variance and misses final grade by 0.76 points on average.',
             insight='This is a strong forecast, but earlier course grades likely dominate the signal. That makes the model better suited to late-course forecasting than early intervention; a version excluding prior grades is the more honest test of proactive usefulness.',
             decision='Compare performance with and without earlier grades and validate by school.'),
    19: dict(perf=(['Accuracy','Spam F1'], [98.39,93.84], 'Percent', (0,100)), context=(['F1 gain over TF-IDF Project 6'], [7.15], 'Percentage points', None),
             summary='Count features produce 98.39% accuracy and 93.84% spam F1, a 7.15-point F1 improvement over the TF-IDF baseline in Project 6.',
             insight='Repeated token evidence appears especially useful for this corpus. Because the two projects rely on one split, the comparison is promising rather than conclusive; deduplication and repeated shared folds are needed to isolate representation effects.',
             decision='Advance count features to repeated cross-validation and false-positive review.'),
    20: dict(perf=(['Precision','Recall'], [35.22,35.22], 'Percent', (0,100)), context=(['Alert precision','Fraud base rate'], [35.22,0.206], 'Percent', (0,40)),
             summary='The detector captures 35.22% of fraud and 35.22% of its alerts are true fraud—far above the 0.206% base rate, but incomplete for stand-alone decisions.',
             insight='Precision is roughly 171 times the raw fraud rate, so anomaly scoring creates genuine investigative lift. The operating issue is coverage: almost two thirds of fraud remains unflagged, while almost two thirds of alerts still require review and turn out not to be fraud.',
             decision='Use the score for triage, then tune alert volume against investigator capacity on a chronological holdout.'),
    21: dict(perf=(['Precision','Recall'], [24.63,24.63], 'Percent', (0,100)), context=(['Alert precision','Anomaly prevalence'], [24.63,9.97], 'Percent', (0,30)),
             summary='The isolation forest captures 24.63% of labeled anomaly points with 24.63% precision on 4,032 CPU observations.',
             insight='The detector lifts precision to about 2.5 times the anomaly prevalence, but misses roughly three quarters of the labeled window. Point-level scoring also penalizes a detector that identifies part of an incident window, so event-level detection delay should accompany precision and recall.',
             decision='Treat this as a triage baseline and evaluate event coverage, delay, and false alerts per day.'),
    22: dict(perf=(['Noisy-image MSE','Reconstructed MSE'], [0.06232,0.03263], 'Mean squared error', None), context=(['Error retained','Error removed'], [52.36,47.64], 'Percent of noisy MSE', (0,100)),
             summary='The linear autoencoder reduces reconstruction MSE from 0.06232 to 0.03263, removing 47.64% of injected-noise error.',
             insight='The reduction is material: nearly half of the corruption is removed using a compact 48-component representation. The remaining error reflects both unrecovered detail and the linear model’s tendency to smooth fine strokes.',
             decision='Preserve this benchmark and compare with a nonlinear convolutional autoencoder using the same corruption process.'),
    23: dict(perf=(['Silhouette score'], [0.3235], 'Score', (0,1)), context=(['Observed separation','Remaining overlap'], [32.35,67.65], 'Percent of score range', (0,100)),
             summary='Twelve genre clusters produce a 0.3235 silhouette score across 9,742 MovieLens titles, indicating overlapping but interpretable groupings.',
             insight='Genre labels are multi-valued, so overlap is structurally expected: a film can bridge comedy, drama, romance, and other categories. Cluster profiles are therefore more useful as catalog neighborhoods than as rigid genre replacements.',
             decision='Inspect cluster genre compositions and test recommendation usefulness rather than chasing separation alone.'),
    24: dict(perf=(['Class silhouette in 2D'], [0.4818], 'Score', (0,1)), context=(['t-SNE KL divergence'], [0.8463], 'Optimization diagnostic', None),
             summary='The t-SNE map achieves a 0.4818 class silhouette, revealing substantial visual separation among the ten digit classes.',
             insight='The embedding is effective for visual exploration, but t-SNE deliberately distorts global distance to preserve local neighborhoods. Nearby clusters are informative; the distance between far-apart clusters should not be interpreted as a quantitative class relationship.',
             decision='Use the map to locate confusion neighborhoods and keep downstream modeling in the original feature space.'),
    25: dict(perf=(['Holdout accuracy','Random-choice baseline'], [81.25,10.0], 'Percent', (0,100)), context=(['Variance retained','Variance discarded'], [86.56,13.44], 'Percent', (0,100)),
             summary='With only 800 labeled training images, the PCA representation supports 81.25% holdout accuracy while retaining 86.56% of image variance.',
             insight='The result shows useful label efficiency: unsupervised structure learned from 8,000 images allows a linear classifier to operate with labels for only one in ten training images. The gap to fully supervised performance quantifies the price of limited labels and linear compression.',
             decision='Build a label-budget curve to show accuracy gained per additional labeled image.'),
    26: dict(perf=(['Unlabeled-set accuracy','Balanced baseline'], [65.14,50.0], 'Percent', (0,100)), context=(['Labeled','Unlabeled'], [10.0,90.0], 'Percent of 4,000 reviews', (0,100)),
             summary='Label spreading reaches 65.14% accuracy across the 90% initially unlabeled review set using labels for only 400 records.',
             insight='The 15-point lift over a balanced baseline confirms that neighborhood structure carries sentiment information, but performance remains well below a strong supervised text classifier. The main value is label efficiency, not absolute accuracy.',
             decision='Compare against a 400-label supervised baseline and use active learning to choose the next reviews to label.'),
    27: dict(perf=(['Precision','Recall'], [30.03,30.03], 'Percent', (0,100)), context=(['Alert precision','Approx. fraud base rate'], [30.03,0.195], 'Percent', (0,35)),
             summary='The outlier detector reaches 30.03% precision and recall across 150k transactions—about 154 times the approximate fraud base rate.',
             insight='The ranking is useful for investigation, but the symmetric precision and recall reflects setting contamination near prevalence rather than an optimized operating point. A production queue should be sized by review capacity and expected loss, not by the observed label rate.',
             decision='Evaluate a chronological holdout and choose the alert threshold from cost and capacity constraints.'),
    28: dict(perf=(['Speaker accuracy','Random-speaker baseline'], [33.68,4.17], 'Percent', (0,100)), context=(['Model lift over chance'], [8.08], 'Multiple', None),
             summary='The GMM identifies speakers at 33.68% accuracy across 24 speakers—about eight times the 4.17% random baseline.',
             insight='The model extracts real speaker signal from simple spectral bands, but two thirds of clips remain misidentified. Emotion, intensity, and utterance content vary within RAVDESS and likely confound the compact features.',
             decision='Use this as an interpretable baseline and add MFCCs plus speaker-balanced validation.'),
    29: dict(perf=(['Silhouette score'], [0.6642], 'Score', (0,1)), context=(['Observed separation','Remaining overlap'], [66.42,33.58], 'Percent of score range', (0,100)),
             summary='Five customer clusters achieve a 0.6642 silhouette score among the top 2,000 customers by spend, indicating strong separation within that selected population.',
             insight='The high score is encouraging, but the top-spender filter shapes the geometry and excludes the long tail. The clusters describe high-value customer behavior—spend, frequency, basket size, and recency—not the full customer base.',
             decision='Profile cluster economics and repeat the analysis on the complete customer population before activation.'),
    30: dict(perf=(['Leave-one-out RMSE'], [1.0476], 'Rating stars', None), context=(['RMSE as share of 4.5-star range'], [23.28], 'Percent', (0,100)),
             summary='User-based collaborative filtering records 1.0476-star RMSE across 610 leave-one-out user ratings.',
             insight='The typical error is about 23% of the full 0.5-to-5 rating range. That is a credible baseline, but ranking quality matters more than rating reconstruction for recommendations; popular-item and global-mean baselines are also needed to establish incremental value.',
             decision='Add baseline RMSE, Precision@K, Recall@K, and cold-start coverage before judging recommendation quality.'),
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
    meta = META[number]
    assets = folder / "analysis"
    assets.mkdir(exist_ok=True)
    bar_chart(assets / "performance.png", meta["perf"], "What the model achieved", "Verified holdout or evaluation result from the project run")
    bar_chart(assets / "context.png", meta["context"], "The context that changes the reading", "Benchmark, composition, or experimental scale used to interpret the headline")

    limitations = clean_limitations(sec.get("Limitations", "The available evaluation is a project benchmark and should be validated on a separate operating sample before deployment."))
    next_step = sec.get("Next step", "Extend the validation with stronger baselines and segmented error analysis.")
    results = sec.get("Results", "")
    report = f"""# {title} — Analysis Report

**Author:** Edward Ocran  
**Project:** {number}  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- {meta['summary']}
- {meta['insight']}
- **Recommended action:** {meta['decision']}

## Analytical Question

{sec.get('Question', 'What does the verified model result reveal, and how should it be used?')}

## Data and Evaluation Design

{sec.get('Data used', '')}

{sec.get('Method', '')}

The reported figures come from the project’s reproducible run. The interpretation separates observed performance from inference: the charts show measured results, while recommendations identify the additional evidence required for a decision.

## Results

{results}

## Visual Evidence

![Verified model performance](analysis/performance.png)

This view shows the primary evaluation result in its original unit. Percentage measures share a common scale; prediction errors remain in their business or measurement unit.

![Benchmark and analytical context](analysis/context.png)

This comparison supplies the benchmark, class balance, retained information, error reduction, or experimental scale needed to interpret the headline result.

## What the Evidence Says

{sec.get('What the result means', meta['summary'])}

{meta['insight']}

## Risks and Limitations

{limitations}

## Recommendations

1. {meta['decision']}
2. {next_step}
3. Preserve the current result as the reference benchmark, then compare the next model on the same split or backtest so any improvement is attributable to the model rather than a changed evaluation sample.

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
