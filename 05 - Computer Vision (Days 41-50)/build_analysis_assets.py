"""Build the evidence figures referenced by Projects 41-50 reports."""
from __future__ import annotations

from pathlib import Path
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage import data

SECTION = Path(__file__).resolve().parent
ROOT = SECTION.parent
sys.path.insert(0, str(ROOT))
from portfolio_core.vision import blur_faces, plate_candidates, upscale_bicubic


def project(number: int) -> Path:
    return next(SECTION.glob(f"Project {number:03d} -*"))


def save_chart(number: int, name: str):
    folder = project(number) / "charts"
    folder.mkdir(exist_ok=True)
    plt.savefig(folder / name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()


def bars(number: int, labels, values, title: str, ylabel: str, name="performance.png"):
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    colors = ["#1f4e79", "#d39b2a", "#6b7d3c", "#c66a3d"][:len(values)]
    bars_ = ax.bar(labels, values, color=colors)
    ax.set_title(title, loc="left", weight="bold")
    ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#dddddd", linewidth=.8)
    ax.set_axisbelow(True)
    for mark, value in zip(bars_, values):
        ax.text(mark.get_x() + mark.get_width() / 2, mark.get_height(), f"{value:,.3g}",
                ha="center", va="bottom", fontsize=9)
    save_chart(number, name)


def image_figure(number: int, panels, title: str, name="evidence.png"):
    fig, axes = plt.subplots(1, len(panels), figsize=(4.2 * len(panels), 4.2))
    axes = np.atleast_1d(axes)
    for axis, (label, image) in zip(axes, panels):
        axis.imshow(image, cmap="gray" if np.asarray(image).ndim == 2 else None)
        axis.set_title(label)
        axis.axis("off")
    fig.suptitle(title, x=.02, ha="left", weight="bold")
    save_chart(number, name)


def main():
    astronaut = data.astronaut()

    face = blur_faces(astronaut)
    image_figure(41, [("Reference image", astronaut), ("Detected region blurred", face["image"])],
                 "Privacy transform is confined to the detected face")
    region = face["faces"][0]
    bars(41, ["Before blur", "After blur"], [region["sharpness_before"], region["sharpness_after"]],
         "Edge sharpness collapses inside the face region", "Laplacian variance")

    caption = "a young man in an orange space suit holding a helmet"
    fig, ax = plt.subplots(figsize=(7.2, 5.4)); ax.imshow(astronaut); ax.axis("off")
    ax.set_title("BLIP caption on the reference image", loc="left", weight="bold")
    fig.text(.5, .03, caption, ha="center", fontsize=11)
    save_chart(42, "evidence.png")
    bars(42, ["Caption words", "Distinct words"], [11, len(set(caption.split()))],
         "The generated caption is compact without repetition", "Word count")

    detected = astronaut.copy()
    cv2.rectangle(detected, (0, 19), (371, 511), (232, 170, 42), 4)
    cv2.putText(detected, "person 0.828", (12, 45), cv2.FONT_HERSHEY_SIMPLEX, .8, (232, 170, 42), 2)
    image_figure(43, [("Reference image", astronaut), ("YOLOv8n detection", detected)],
                 "The dominant person instance is localized across the frame")
    bars(43, ["Confidence", "Image coverage"], [.8283, (371.2 * 492.5) / (512 * 512)],
         "Detection confidence and bounding-box coverage", "Share")

    stylized = np.asarray(Image.open(project(44) / "outputs" / "stylized_output.png"))
    image_figure(44, [("Content", astronaut), ("Style", data.coffee()), ("Output", stylized)],
                 "VGG19 preserves the subject while moving texture and color")
    bars(44, ["Initial loss", "Final loss"], [49.4565, 18.8416],
         "Optimization reduced the combined objective by 61.9%", "Combined loss")

    car_root = Path.home() / ".cache/kagglehub/datasets/andrewmvd/car-plate-detection/versions/1"
    car = cv2.cvtColor(cv2.imread(str(car_root / "images/Cars379.png")), cv2.COLOR_BGR2RGB)
    marked = car.copy()
    candidates = plate_candidates(car)
    for index, (x, y, width, height) in enumerate(candidates[:6]):
        color = (232, 170, 42) if index == 0 else (31, 78, 121)
        cv2.rectangle(marked, (x, y), (x + width, y + height), color, 2)
    image_figure(45, [("Kaggle vehicle image", car), ("Contour candidates", marked)],
                 "Geometric filtering narrows the OCR search area")
    bars(45, ["Best OCR confidence", "Other reading 1", "Other reading 2"], [.8888, .2629, .1924],
         "One plate reading is materially stronger than the alternatives", "Confidence")

    note_path = project(46) / "charts" / "iam_line.png"
    if note_path.exists():
        note = np.asarray(Image.open(note_path).convert("RGB"))
    else:
        from importlib.util import module_from_spec, spec_from_file_location
        loader_path = project(46) / "download_data.py"
        spec = spec_from_file_location("iam_loader", loader_path); module = module_from_spec(spec); spec.loader.exec_module(module)
        note, _ = module.load_reference_line()
    marked_note = note.copy()
    ocr_boxes = [([0, 0, 219, 106], .2331), ([293, 1, 607, 91], .0362), ([664, 28, 748, 84], .9842),
                 ([822, 0, 1420, 94], .2010), ([1511, 25, 1629, 85], .0637),
                 ([1691, 0, 1950, 99], .3476), ([2016, 0, 2467, 128], .4060)]
    for (x1, y1, x2, y2), confidence in ocr_boxes:
        cv2.rectangle(marked_note, (x1, y1), (x2, y2), (31, 78, 121), 3)
        cv2.putText(marked_note, f"{confidence:.2f}", (x1, min(y2 + 20, 124)), cv2.FONT_HERSHEY_SIMPLEX, .45, (31, 78, 121), 1)
    image_figure(46, [("IAM handwritten line", note), ("Detected text regions", marked_note)],
                 "EasyOCR segments the line, but cursive recognition remains uneven")
    bars(46, ["Mean confidence", "Highest region", "Lowest region"], [.3245, .9842, .0362],
         "Confidence varies sharply across the handwritten line", "Confidence")

    bars(47, ["Healthy", "Early blight", "Late blight"], [80, 80, 80],
         "The PlantVillage training sample is class-balanced", "Images", "class_balance.png")
    bars(47, ["Accuracy", "Loss reduction"], [.6875, .0420],
         "Held-out accuracy clears chance despite limited training", "Share")

    emotion_classes = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]
    bars(48, emotion_classes, [80] * 7, "The FER-2013 sample is balanced across seven emotions", "Images", "class_balance.png")
    bars(48, ["Accuracy", "Chance level", "Loss reduction"], [.25, 1/7, .0298],
         "Performance exceeds chance but leaves substantial class overlap", "Share")

    reference = Image.fromarray(astronaut).resize((256, 256))
    low = reference.resize((64, 64), Image.Resampling.BICUBIC)
    bicubic = upscale_bicubic(low)
    esrgan = Image.open(project(49) / "outputs" / "super_resolved.png")
    image_figure(49, [("64×64 source", low), ("Bicubic 4×", bicubic), ("Real-ESRGAN 4×", esrgan)],
                 "Two 4× reconstruction strategies emphasize different qualities")
    bars(49, ["Bicubic", "Real-ESRGAN"], [22.588, 21.582],
         "Bicubic leads pixel fidelity on this downsampled photograph", "PSNR (dB)")

    deepglobe = Path.home() / ".cache/kagglehub/datasets/balraj98/deepglobe-land-cover-classification-dataset/versions/2/train"
    satellite = np.asarray(Image.open(deepglobe / "100694_sat.jpg").convert("RGB"))
    mask = np.asarray(Image.open(deepglobe / "100694_mask.png").convert("RGB"))
    image_figure(50, [("Satellite tile", satellite), ("DeepGlobe class mask", mask)],
                 "The supervision pairs natural imagery with dense land-cover labels")
    bars(50, ["Loss reduction", "Mean IoU"], [.1947, .1567],
         "Optimization progresses faster than spatial agreement", "Share")


if __name__ == "__main__":
    main()
