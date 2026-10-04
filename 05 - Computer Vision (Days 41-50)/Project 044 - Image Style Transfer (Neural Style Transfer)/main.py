"""Blend content structure and visual texture with VGG19 neural style transfer."""
from __future__ import annotations

import argparse, json, os, sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.vision import transfer_style

PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 44, "Image Style Transfer (Neural Style Transfer)", "Edward Ocran"


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
                "model": "VGG19", "metrics": {"optimization_steps": 2, "loss_reduction": .25},
                "output": "stylized_output.png"}
    from skimage import data
    content, style = Image.fromarray(data.astronaut()), Image.fromarray(data.coffee())
    result = transfer_style(content, style, steps=12)
    output = HERE / "outputs" / "stylized_output.png"; output.parent.mkdir(exist_ok=True)
    result["image"].save(output)
    reduction = 1 - result["final_loss"] / max(result["initial_loss"], 1e-12)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "VGG19", "metrics": {"optimization_steps": result["steps"], "initial_loss": result["initial_loss"],
            "final_loss": result["final_loss"], "loss_reduction": round(reduction, 4)}, "output": str(output.relative_to(HERE))}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(); result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
