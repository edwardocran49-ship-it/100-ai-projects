"""Support-vector classification on the complete handwritten-digits dataset."""
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

PROJECT_TITLE = "SVM for Handwritten Digit Recognition"

def run_demo():
    data = load_digits()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=.2, random_state=42, stratify=data.target)
    model = make_pipeline(StandardScaler(), SVC(C=5, gamma="scale")).fit(X_train, y_train)
    pred = model.predict(X_test)
    return {"project": 7, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Optical Recognition of Handwritten Digits", "records": len(data.data), "metrics": {"accuracy": round(float(accuracy_score(y_test, pred)), 4), "macro_f1": round(float(f1_score(y_test, pred, average="macro")), 4)}, "confusion_matrix": confusion_matrix(y_test, pred).tolist()}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
