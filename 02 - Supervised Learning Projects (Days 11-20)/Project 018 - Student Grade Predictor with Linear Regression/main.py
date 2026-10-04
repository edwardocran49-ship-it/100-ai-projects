"""Student final-grade regression on the UCI Portuguese course data."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge
from download_data import ensure_dataset

PROJECT_TITLE = "Student Grade Predictor with Linear Regression"

def run_demo():
    df = pd.read_csv(ensure_dataset())
    X, y = df.drop(columns="G3"), df.G3
    categorical = X.select_dtypes(exclude="number").columns.tolist(); numeric = X.select_dtypes(include="number").columns.tolist()
    prep = ColumnTransformer([("num", StandardScaler(), numeric), ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
    model = make_pipeline(prep, Ridge(alpha=5)).fit(X_train, y_train); pred = model.predict(X_test)
    return {"project": 18, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "UCI Student Performance (Portuguese)", "records": len(df), "metrics": {"mae_grade_points": round(float(mean_absolute_error(y_test, pred)), 4), "r2": round(float(r2_score(y_test, pred)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
