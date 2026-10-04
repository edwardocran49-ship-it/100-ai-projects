"""Multinomial Naive Bayes classifier on real SMS messages."""
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

PROJECT_TITLE = "Naive Bayes Text Classifier"
from download_data import ensure_dataset

DATA = Path(__file__).with_name("data") / "spam.csv"

def run_demo():
    ensure_dataset()
    df = pd.read_csv(DATA, encoding="latin-1")[["v1", "v2"]].dropna()
    X_train, X_test, y_train, y_test = train_test_split(df.v2, df.v1, test_size=.2, random_state=42, stratify=df.v1)
    model = make_pipeline(TfidfVectorizer(stop_words="english"), MultinomialNB()).fit(X_train, y_train)
    pred = model.predict(X_test)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, pred, average="binary", pos_label="spam", zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=["ham", "spam"]).ravel()
    return {"project": 6, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "SMS Spam Collection", "records": len(df), "metrics": {"accuracy": round(float(accuracy_score(y_test, pred)), 4), "spam_precision": round(float(precision), 4), "spam_recall": round(float(recall), 4), "spam_f1": round(float(f1), 4), "true_negative": int(tn), "false_positive": int(fp), "false_negative": int(fn), "true_positive": int(tp)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
