"""Customer segmentation using the downloaded Mall Customers data."""
from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

PROJECT_TITLE = "K-Means Clustering for Customer Segmentation"
from download_data import ensure_dataset

DATA = Path(__file__).with_name("data") / "Mall_Customers.csv"

def run_demo():
    ensure_dataset()
    df = pd.read_csv(DATA)
    X = df[["Annual Income (k$)", "Spending Score (1-100)"]]
    scaled = StandardScaler().fit_transform(X)
    labels = KMeans(n_clusters=5, n_init=20, random_state=42).fit_predict(scaled)
    return {"project": 3, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Mall Customers", "records": len(df), "clusters": 5, "metrics": {"silhouette": round(float(silhouette_score(scaled, labels)), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
