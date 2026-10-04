"""Computer-vision implementations shared by Projects 41-50."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import numpy as np


def blur_faces(image: np.ndarray, detector=None, kernel: int = 99) -> dict[str, Any]:
    import cv2

    if detector is None:
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    output = image.copy()
    regions = []
    for x, y, width, height in faces:
        roi = output[y:y + height, x:x + width]
        before = float(cv2.Laplacian(roi, cv2.CV_64F).var())
        size = min(kernel, width if width % 2 else width - 1, height if height % 2 else height - 1)
        size = max(3, size if size % 2 else size - 1)
        blurred = cv2.GaussianBlur(roi, (size, size), 30)
        output[y:y + height, x:x + width] = blurred
        after = float(cv2.Laplacian(blurred, cv2.CV_64F).var())
        regions.append({"x": int(x), "y": int(y), "width": int(width), "height": int(height),
                        "sharpness_before": round(before, 2), "sharpness_after": round(after, 2)})
    return {"image": output, "faces": regions}


def caption_image(image, backend: Callable[[Any], str] | None = None) -> str:
    if backend is not None:
        return str(backend(image)).strip()
    from transformers import BlipForConditionalGeneration, BlipProcessor

    model_name = "Salesforce/blip-image-captioning-base"
    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)
    inputs = processor(images=image, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=30)
    return processor.decode(output[0], skip_special_tokens=True).strip()


def detect_objects(image, backend=None) -> list[dict[str, Any]]:
    if backend is not None:
        return list(backend(image))
    from ultralytics import YOLO

    model = YOLO("yolov8n.pt")
    result = model.predict(source=np.asarray(image), verbose=False)[0]
    detections = []
    for box in result.boxes:
        class_id = int(box.cls.item())
        detections.append({"label": model.names[class_id], "confidence": round(float(box.conf.item()), 4),
                           "box": [round(float(value), 1) for value in box.xyxy[0].tolist()]})
    return detections


def gram_matrix(tensor):
    import torch

    batch, channels, height, width = tensor.shape
    features = tensor.view(batch * channels, height * width)
    return torch.mm(features, features.t()) / (batch * channels * height * width)


def transfer_style(content, style, steps: int = 30, image_size: int = 128) -> dict[str, Any]:
    import torch
    from PIL import Image
    from torchvision import models, transforms

    convert = transforms.Compose([transforms.Resize((image_size, image_size)), transforms.ToTensor()])
    content_tensor = convert(content.convert("RGB")).unsqueeze(0)
    style_tensor = convert(style.convert("RGB")).unsqueeze(0)
    weights = models.VGG19_Weights.DEFAULT
    vgg = models.vgg19(weights=weights).features.eval()
    for parameter in vgg.parameters():
        parameter.requires_grad = False
    chosen = {"0", "5", "10", "19", "21", "28"}

    def features(value):
        found = {}
        for name, layer in vgg._modules.items():
            value = layer(value)
            if name in chosen:
                found[name] = value
        return found

    content_features = features(content_tensor)
    style_features = features(style_tensor)
    generated = content_tensor.clone().requires_grad_(True)
    optimizer = torch.optim.Adam([generated], lr=.02)
    losses = []
    for _ in range(steps):
        generated_features = features(generated)
        content_loss = torch.mean((generated_features["21"] - content_features["21"]) ** 2)
        style_loss = sum(torch.mean((gram_matrix(generated_features[layer]) - gram_matrix(style_features[layer])) ** 2)
                         for layer in ("0", "5", "10", "19", "28"))
        total = content_loss + 1e6 * style_loss
        optimizer.zero_grad()
        total.backward()
        optimizer.step()
        with torch.no_grad():
            generated.clamp_(0, 1)
        losses.append(float(total.item()))
    output = transforms.ToPILImage()(generated.detach().squeeze(0))
    return {"image": output, "initial_loss": losses[0], "final_loss": losses[-1], "steps": steps}


def plate_candidates(image: np.ndarray) -> list[tuple[int, int, int, int]]:
    import cv2

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        ratio = width / float(max(height, 1))
        if 2 < ratio < 6 and width >= 80 and height >= 20:
            candidates.append((x, y, width, height))
    return sorted(candidates, key=lambda item: item[2] * item[3], reverse=True)


def read_text(image: np.ndarray, reader=None) -> list[dict[str, Any]]:
    if reader is None:
        import easyocr
        reader = easyocr.Reader(["en"], gpu=False)
    results = reader.readtext(image)
    return [{"text": str(text), "confidence": round(float(confidence), 4),
             "box": [[round(float(x), 1), round(float(y), 1)] for x, y in box]}
            for box, text, confidence in results]


def upscale_bicubic(image, scale: int = 4):
    from PIL import Image

    return image.resize((image.width * scale, image.height * scale), Image.Resampling.BICUBIC)


def super_resolve_esrgan(image, backend=None):
    if backend is not None:
        return backend(image)
    import sys
    import types
    from PIL import Image
    from torchvision.transforms.functional import rgb_to_grayscale

    compatibility = types.ModuleType("torchvision.transforms.functional_tensor")
    compatibility.rgb_to_grayscale = rgb_to_grayscale
    sys.modules.setdefault(compatibility.__name__, compatibility)
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer

    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23,
                    num_grow_ch=32, scale=4)
    weights = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
    upsampler = RealESRGANer(scale=4, model_path=weights, model=model, tile=0,
                            tile_pad=10, pre_pad=0, half=False)
    bgr = np.asarray(image.convert("RGB"))[:, :, ::-1]
    output, _ = upsampler.enhance(bgr, outscale=4)
    return Image.fromarray(output[:, :, ::-1])


def psnr(reference, candidate) -> float:
    reference_array = np.asarray(reference, dtype=float)
    candidate_array = np.asarray(candidate.resize(reference.size), dtype=float)
    mse = float(np.mean((reference_array - candidate_array) ** 2))
    return float("inf") if mse == 0 else round(20 * np.log10(255.0 / np.sqrt(mse)), 3)


def train_tiny_classifier(images: np.ndarray, labels: np.ndarray, epochs: int = 2) -> dict[str, Any]:
    """Train the PDF-specified two-layer CNN on an in-memory image sample."""
    import torch
    import torch.nn as nn
    from sklearn.model_selection import train_test_split

    x_train, x_test, y_train, y_test = train_test_split(
        images, labels, test_size=.2, random_state=42, stratify=labels
    )
    x_train = torch.tensor(x_train, dtype=torch.float32)
    x_test = torch.tensor(x_test, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.long)
    y_test = torch.tensor(y_test, dtype=torch.long)
    channels, height, width = x_train.shape[1:]

    class CNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.features = nn.Sequential(nn.Conv2d(channels, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                                          nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2))
            self.classifier = nn.Linear(32 * (height // 4) * (width // 4), int(labels.max()) + 1)

        def forward(self, value):
            return self.classifier(self.features(value).flatten(1))

    torch.manual_seed(42)
    model = CNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=.001)
    criterion = nn.CrossEntropyLoss()
    losses = []
    for _ in range(epochs):
        optimizer.zero_grad()
        output = model(x_train)
        loss = criterion(output, y_train)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.item()))
    with torch.no_grad():
        predicted = model(x_test).argmax(1)
    accuracy = float((predicted == y_test).float().mean().item())
    return {"model": model, "accuracy": round(accuracy, 4), "initial_loss": round(losses[0], 4),
            "final_loss": round(losses[-1], 4), "train_records": len(x_train), "test_records": len(x_test)}


def mean_iou(expected: np.ndarray, predicted: np.ndarray, classes: int) -> float:
    scores = []
    for label in range(classes):
        intersection = np.logical_and(expected == label, predicted == label).sum()
        union = np.logical_or(expected == label, predicted == label).sum()
        if union:
            scores.append(intersection / union)
    return round(float(np.mean(scores)), 4) if scores else 0.0


def train_tiny_segmenter(images: np.ndarray, masks: np.ndarray, classes: int, epochs: int = 5) -> dict[str, Any]:
    """Train a compact encoder-decoder segmentation network on image/mask pairs."""
    import torch
    import torch.nn as nn

    torch.manual_seed(42)
    x = torch.tensor(images, dtype=torch.float32)
    y = torch.tensor(masks, dtype=torch.long)

    class MiniUNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = nn.Sequential(nn.Conv2d(x.shape[1], 16, 3, padding=1), nn.ReLU(),
                                         nn.Conv2d(16, 16, 3, padding=1), nn.ReLU())
            self.pool = nn.MaxPool2d(2)
            self.middle = nn.Sequential(nn.Conv2d(16, 32, 3, padding=1), nn.ReLU())
            self.up = nn.ConvTranspose2d(32, 16, 2, stride=2)
            self.head = nn.Conv2d(32, classes, 1)

        def forward(self, value):
            skip = self.encoder(value)
            middle = self.middle(self.pool(skip))
            return self.head(torch.cat([self.up(middle), skip], dim=1))

    model = MiniUNet()
    optimizer = torch.optim.Adam(model.parameters(), lr=.003)
    criterion = nn.CrossEntropyLoss()
    losses = []
    for _ in range(epochs):
        output = model(x)
        loss = criterion(output, y)
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        losses.append(float(loss.item()))
    with torch.no_grad():
        predicted = model(x).argmax(1).numpy()
    return {"model": model, "prediction": predicted, "initial_loss": round(losses[0], 4),
            "final_loss": round(losses[-1], 4), "mean_iou": mean_iou(masks, predicted, classes)}
