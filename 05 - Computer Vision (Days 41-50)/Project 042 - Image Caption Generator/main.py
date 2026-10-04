"""Generate natural-language image descriptions with pretrained BLIP."""
from __future__ import annotations

import argparse, json, os, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.vision import caption_image

PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 42, "Image Caption Generator", "Edward Ocran"


def _validation_backend(image):
    return "an astronaut wearing a white suit"


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        image = Image.new("RGB", (64, 64), "navy")
    else:
        from skimage import data
        image = Image.fromarray(data.astronaut())
    caption = caption_image(image, backend=_validation_backend if fast else None)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "Salesforce/blip-image-captioning-base", "caption": caption,
            "metrics": {"caption_words": len(caption.split()), "image_width": image.width, "image_height": image.height}}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(); result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
