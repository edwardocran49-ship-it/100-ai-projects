"""Upscale a low-resolution image with a pretrained ESRGAN generator."""
from __future__ import annotations

import argparse, json, os, sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from portfolio_core.vision import psnr, super_resolve_esrgan, upscale_bicubic

PROJECT_NUMBER, PROJECT_TITLE, AUTHOR = 49, "Image Super-Resolution with SRGAN", "Edward Ocran"


def _validation_backend(image):
    return image.resize((image.width * 4, image.height * 4), Image.Resampling.BICUBIC)


def run_demo(fast: bool | None = None) -> dict:
    fast = os.getenv("PORTFOLIO_FAST_VALIDATION") == "1" if fast is None else fast
    if fast:
        reference = Image.new("RGB", (64, 64), "teal")
    else:
        from skimage import data
        reference = Image.fromarray(data.astronaut()).resize((256, 256))
    low = reference.resize((reference.width // 4, reference.height // 4), Image.Resampling.BICUBIC)
    output = super_resolve_esrgan(low, backend=_validation_backend if fast else None)
    if not fast:
        folder = HERE / "outputs"; folder.mkdir(exist_ok=True); output.save(folder / "super_resolved.png")
    baseline = upscale_bicubic(low)
    return {"project": PROJECT_NUMBER, "title": PROJECT_TITLE, "author": AUTHOR, "status": "ok",
            "model": "Real-ESRGAN x4plus", "metrics": {"scale_factor": 4, "output_width": output.width,
            "output_height": output.height, "esrgan_psnr": psnr(reference, output),
            "bicubic_psnr": psnr(reference, baseline)}}


def main():
    parser = argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json", action="store_true")
    args = parser.parse_args(); result = run_demo()
    print(json.dumps(result, sort_keys=True) if args.json else json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
