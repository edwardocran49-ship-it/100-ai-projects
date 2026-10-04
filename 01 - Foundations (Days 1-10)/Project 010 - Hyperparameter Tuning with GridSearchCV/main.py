"""SVM hyperparameter selection on the Iris dataset."""
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

PROJECT_TITLE = "Hyperparameter Tuning with GridSearchCV"

def run_demo():
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=.2, random_state=42, stratify=data.target)
    search = GridSearchCV(make_pipeline(StandardScaler(), SVC()), {"svc__C": [.1, 1, 10], "svc__kernel": ["linear", "rbf"], "svc__gamma": ["scale", "auto"]}, cv=5, n_jobs=1).fit(X_train, y_train)
    return {"project": 10, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Iris", "records": len(data.data), "best_parameters": search.best_params_, "metrics": {"accuracy": round(float(accuracy_score(y_test, search.predict(X_test))), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
