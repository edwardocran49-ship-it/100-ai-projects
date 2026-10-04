"""Random-forest diagnosis baseline on the Wisconsin breast-cancer data."""
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split

PROJECT_TITLE = "Random Forest on Breast Cancer Dataset"

def run_demo():
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=.2, random_state=42, stratify=data.target)
    model = RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=1).fit(X_train, y_train)
    pred = model.predict(X_test)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, pred, average="binary", zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
    top_features = sorted(zip(data.feature_names, model.feature_importances_), key=lambda pair: pair[1], reverse=True)[:5]
    return {"project": 5, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Breast Cancer Wisconsin Diagnostic", "records": len(data.data), "metrics": {"accuracy": round(float(accuracy_score(y_test, pred)), 4), "precision": round(float(precision), 4), "recall": round(float(recall), 4), "f1": round(float(f1), 4), "true_negative": int(tn), "false_positive": int(fp), "false_negative": int(fn), "true_positive": int(tp)}, "top_features": [{"feature": str(name), "importance": round(float(value), 4)} for name, value in top_features]}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
