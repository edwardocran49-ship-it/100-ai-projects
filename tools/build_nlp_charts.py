"""Build evidence charts for the verified NLP projects (31-40)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1] / "04 - NLP Projects (Days 31-40)"
COLORS = ["#1f4e79", "#2a9d8f", "#e9c46a", "#e76f51", "#6d597a", "#457b9d"]


def project(number: int) -> Path:
    return next(ROOT.glob(f"Project {number:03d} -*"))


def save(number: int, name: str):
    folder = project(number) / "charts"
    folder.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(folder / name, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def bars(number, name, labels, values, title, ylabel="Value", percent=False):
    plt.figure(figsize=(7.2, 4.2))
    items = plt.bar(labels, values, color=COLORS[:len(values)])
    plt.title(title, loc="left", weight="bold")
    plt.ylabel(ylabel)
    if percent:
        plt.ylim(0, 1.08)
    plt.grid(axis="y", alpha=.2)
    for bar, value in zip(items, values):
        label = f"{value:.1%}" if percent else f"{value:g}"
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), label, ha="center", va="bottom")
    save(number, name)


def heatmap(number, name, matrix, labels, title):
    plt.figure(figsize=(5.8, 4.8))
    plt.imshow(matrix, cmap="Blues")
    plt.xticks(range(len(labels)), labels)
    plt.yticks(range(len(labels)), labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(title, loc="left", weight="bold")
    for row in range(len(labels)):
        for col in range(len(labels)):
            plt.text(col, row, str(matrix[row][col]), ha="center", va="center", fontsize=13)
    plt.colorbar(shrink=.75)
    save(number, name)


heatmap(31, "confusion_matrix.png", [[94, 6], [12, 88]], ["Negative", "Positive"], "IMDb sentiment confusion matrix")
bars(31, "model_metrics.png", ["Accuracy", "Precision", "Recall", "F1"], [.91, .9362, .88, .9072], "BERT evaluation metrics", percent=True)

bars(32, "text_length.png", ["Source", "Summary"], [42, 23], "Text length before and after summarization", "Words")
bars(32, "compression.png", ["Retained", "Removed"], [.548, .452], "Summary compression profile", "Share of source words", True)

bars(33, "answer_confidence.png", ["Answer", "Remaining uncertainty"], [.972, .028], "Extractive answer confidence", "Probability", True)
bars(33, "answer_span.png", ["Before answer", "Answer span", "After answer"], [47, 16, 67], "Where the answer appears in the context", "Characters")

heatmap(34, "confusion_matrix.png", [[966, 0], [35, 114]], ["Ham", "Spam"], "Spam classifier confusion matrix")
bars(34, "model_metrics.png", ["Accuracy", "Precision", "Recall", "F1"], [.9686, 1.0, .7651, .8669], "Spam classification metrics", percent=True)

bars(35, "field_coverage.png", ["Name", "Email", "Phone", "Skills", "Education", "Experience"], [1, 1, 1, 1, 1, 1], "Resume field extraction coverage", "Extracted")
bars(35, "skills_found.png", ["Python", "SQL", "Excel", "Tableau", "ML", "Analysis"], [1, 1, 1, 1, 1, 1], "Skills identified in the sample resume", "Matches")

bars(36, "entity_mix.png", ["PERSON", "ORG", "GPE", "DATE"], [1, 1, 1, 1], "Entities recovered by label", "Entities")
bars(36, "entity_span.png", ["Satya Nadella", "Microsoft", "London", "14 March 2025"], [13, 9, 6, 13], "Entity span lengths", "Characters")

bars(37, "search_ranking.png", ["Battery storage", "Solar panels", "Wind turbines"], [.6407, .5228, .4144], "Semantic-search relevance ranking", "Cosine similarity")
bars(37, "score_gaps.png", ["Rank 1–2 gap", "Rank 2–3 gap"], [.1179, .1084], "Separation between adjacent results", "Similarity points")

bars(38, "label_confidence.png", ["Economy", "Health", "Technology", "Sports"], [.7092, .1220, .1099, .0589], "Zero-shot classification confidence", "Probability", True)
bars(38, "decision_margin.png", ["Top label", "Runner-up", "Margin"], [.7092, .1220, .5872], "Decision strength", "Probability", True)

bars(39, "conversation_size.png", ["History turns", "Prompt words", "Response words"], [1, 7, 10], "Conversation footprint", "Count")
bars(39, "response_profile.png", ["Input words", "Output words", "Output/Input"], [7, 10, 1.43], "Generated response profile", "Value")

bars(40, "translation_length.png", ["English source", "French output"], [7, 11], "Translation length by language", "Words")
bars(40, "reference_check.png", ["Token overlap", "Unmatched share"], [1.0, 0.0], "Reference token coverage", "Share", True)

print("Built 20 charts for Projects 31-40")
