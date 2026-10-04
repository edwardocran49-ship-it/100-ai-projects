"""Principal-component analysis of the handwritten-digits dataset."""
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

PROJECT_TITLE = "PCA for Dimensionality Reduction"

def run_demo():
    data = load_digits()
    scaled = StandardScaler().fit_transform(data.data)
    pca = PCA(n_components=2, random_state=42).fit(scaled)
    transformed = pca.transform(scaled)
    return {"project": 8, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "Optical Recognition of Handwritten Digits", "records": len(data.data), "input_dimensions": data.data.shape[1], "output_dimensions": transformed.shape[1], "metrics": {"explained_variance": round(float(pca.explained_variance_ratio_.sum()), 4)}}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
