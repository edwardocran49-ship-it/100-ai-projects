"""Voice-gender classification from measured acoustic features."""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from download_data import ensure_dataset

PROJECT_TITLE = "Voice Gender Classifier"

def run_demo():
    df = pd.read_csv(ensure_dataset())
    X, y = df.drop(columns="label"), df.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=180, random_state=42, n_jobs=1).fit(X_train, y_train)
    return {"project": 16, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Gender Recognition by Voice", "records": len(df), "metrics": {"accuracy": round(float(accuracy_score(y_test, model.predict(X_test))), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
