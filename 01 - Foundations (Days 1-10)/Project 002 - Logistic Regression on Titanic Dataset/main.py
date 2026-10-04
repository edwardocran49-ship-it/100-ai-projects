"""Titanic survival classification using the downloaded Kaggle data."""
from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_TITLE = "Logistic Regression on Titanic Dataset"
from download_data import ensure_dataset

DATA = Path(__file__).with_name("data") / "titanic.csv"

def run_demo():
    ensure_dataset()
    df = pd.read_csv(DATA)
    features = ["Age", "Fare", "Sex", "sibsp", "Parch", "Pclass", "Embarked"]
    X, y = df[features], df["2urvived"]
    numeric = ["Age", "Fare", "sibsp", "Parch"]
    categorical = ["Sex", "Pclass", "Embarked"]
    prep = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
        ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), categorical),
    ])
    model = make_pipeline(prep, LogisticRegression(max_iter=1000))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, pred, average="binary", zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
    return {"project": 2, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Titanic", "records": len(df), "metrics": {"accuracy": round(float(accuracy_score(y_test, pred)), 4), "precision": round(float(precision), 4), "recall": round(float(recall), 4), "f1": round(float(f1), 4), "true_negative": int(tn), "false_positive": int(fp), "false_negative": int(fn), "true_positive": int(tp)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
