"""XGBoost classification on the UCI-derived heart-disease data."""
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from download_data import ensure_dataset

PROJECT_TITLE = "Predict Heart Disease with XGBoost"

def run_demo():
    df = pd.read_csv(ensure_dataset())
    X, y = df.drop(columns="target"), df.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model = XGBClassifier(n_estimators=120, max_depth=3, learning_rate=.08, subsample=.9, colsample_bytree=.9, random_state=42, eval_metric="logloss", n_jobs=1).fit(X_train, y_train)
    prediction = model.predict(X_test); probability = model.predict_proba(X_test)[:, 1]
    return {"project": 14, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Heart Disease Dataset", "records": len(df), "metrics": {"accuracy": round(float(accuracy_score(y_test, prediction)), 4), "roc_auc": round(float(roc_auc_score(y_test, probability)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
