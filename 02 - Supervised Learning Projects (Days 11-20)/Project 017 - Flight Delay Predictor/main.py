"""Flight-delay prediction on a real U.S. Department of Transportation sample."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import HistGradientBoostingClassifier
from download_data import ensure_dataset

PROJECT_TITLE = "Flight Delay Predictor"

def run_demo():
    use = ["MONTH", "DAY", "DAY_OF_WEEK", "AIRLINE", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT", "SCHEDULED_DEPARTURE", "DISTANCE", "ARRIVAL_DELAY", "CANCELLED"]
    df = pd.read_csv(ensure_dataset(), usecols=use, nrows=75000).query("CANCELLED == 0").dropna(subset=["ARRIVAL_DELAY"])
    y = (df.pop("ARRIVAL_DELAY") > 15).astype(int); df = df.drop(columns="CANCELLED")
    categorical = ["AIRLINE", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT"]
    numeric = [c for c in df.columns if c not in categorical]
    prep = ColumnTransformer([("num", SimpleImputer(strategy="median"), numeric), ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore", min_frequency=20, sparse_output=False)), categorical)])
    model = make_pipeline(prep, HistGradientBoostingClassifier(max_iter=100, random_state=42))
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=.2, random_state=42, stratify=y)
    model.fit(X_train, y_train); pred = model.predict(X_test)
    return {"project": 17, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "2015 Flight Delays and Cancellations", "records": len(df), "metrics": {"accuracy": round(float(accuracy_score(y_test, pred)), 4), "delay_f1": round(float(f1_score(y_test, pred)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
