"""Credit-risk classification using the German Credit data with its target."""
from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

PROJECT_TITLE = "Decision Tree Classifier for Credit Risk"
DATA = Path(__file__).with_name("data") / "german_credit_data.csv"

def run_demo():
    df = pd.read_csv(DATA).drop(columns=["Unnamed: 0"], errors="ignore")
    X, y = df.drop(columns="Risk"), df["Risk"]
    categorical = X.select_dtypes(exclude="number").columns.tolist()
    numeric = X.select_dtypes(include="number").columns.tolist()
    prep = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), numeric),
        ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), categorical),
    ])
    model = make_pipeline(prep, DecisionTreeClassifier(max_depth=5, random_state=42))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model.fit(X_train, y_train)
    return {"project": 4, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "German Credit Risk", "records": len(df), "metrics": {"accuracy": round(float(accuracy_score(y_test, model.predict(X_test))), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
