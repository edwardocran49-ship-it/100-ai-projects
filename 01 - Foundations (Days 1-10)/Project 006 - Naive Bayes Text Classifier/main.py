"""Multinomial Naive Bayes classifier on real SMS messages."""
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score
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
    return {"project": 6, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "SMS Spam Collection", "records": len(df), "metrics": {"accuracy": round(float(accuracy_score(y_test, pred)), 4), "spam_f1": round(float(f1_score(y_test, pred, pos_label="spam")), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
