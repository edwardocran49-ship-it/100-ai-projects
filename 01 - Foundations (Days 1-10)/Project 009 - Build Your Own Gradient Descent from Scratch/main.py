"""Univariate linear regression trained with gradient descent from scratch."""
import random

PROJECT_TITLE = "Build Your Own Gradient Descent from Scratch"

def run_demo():
    rng = random.Random(42)
    xs = [i / 10 for i in range(100)]
    ys = [3.2 * x + 4.5 + rng.uniform(-.25, .25) for x in xs]
    slope = intercept = 0.0
    rate = .003
    loss_history = []
    for iteration in range(5000):
        errors = [(slope * x + intercept) - y for x, y in zip(xs, ys)]
        if iteration % 250 == 0:
            loss_history.append(round(sum(error ** 2 for error in errors) / len(errors), 6))
        slope -= rate * (2 / len(xs)) * sum(error * x for error, x in zip(errors, xs))
        intercept -= rate * (2 / len(xs)) * sum(errors)
    mse = sum((slope * x + intercept - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
    loss_history.append(round(mse, 6))
    return {"project": 9, "title": PROJECT_TITLE, "author": "Edward Ocran", "status": "ok", "dataset": "course-generated linear observations", "records": len(xs), "metrics": {"initial_mse": loss_history[0], "final_mse": round(mse, 6), "slope": round(slope, 4), "intercept": round(intercept, 4)}, "loss_history": loss_history}

def main() -> None:
    import argparse, json
    parser = argparse.ArgumentParser(description=PROJECT_TITLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
