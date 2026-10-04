"""Small, inspectable audio utilities used by Projects 61-70."""
from __future__ import annotations

import math
import wave
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.fft import dct
from scipy.io import wavfile
from scipy.signal import resample_poly, spectrogram


def load_wav(path: str | Path, target_rate: int = 16000) -> tuple[int, np.ndarray]:
    """Load PCM WAV as normalized mono float samples."""
    rate, samples = wavfile.read(path)
    if samples.ndim > 1:
        samples = samples.mean(axis=1)
    if np.issubdtype(samples.dtype, np.integer):
        scale = max(abs(np.iinfo(samples.dtype).min), np.iinfo(samples.dtype).max)
        samples = samples.astype(np.float32) / scale
    else:
        samples = samples.astype(np.float32)
    if rate != target_rate and len(samples):
        divisor = math.gcd(rate, target_rate)
        samples = resample_poly(samples, target_rate // divisor, rate // divisor).astype(np.float32)
        rate = target_rate
    return rate, samples


def audio_features(path: str | Path) -> np.ndarray:
    """Extract stable time, spectral, and cepstral summary features."""
    rate, values = load_wav(path)
    if not len(values):
        raise ValueError("Audio file is empty")
    values = values - values.mean()
    rms = float(np.sqrt(np.mean(values ** 2)))
    zcr = float(np.mean(np.signbit(values[1:]) != np.signbit(values[:-1])))
    spectrum = np.abs(np.fft.rfft(values * np.hanning(len(values)))) + 1e-10
    frequencies = np.fft.rfftfreq(len(values), 1 / rate)
    weights = spectrum / spectrum.sum()
    centroid = float(np.sum(frequencies * weights) / (rate / 2))
    bandwidth = float(np.sqrt(np.sum(((frequencies - centroid * rate / 2) ** 2) * weights)) / (rate / 2))
    cumulative = np.cumsum(weights)
    rolloff = float(frequencies[min(np.searchsorted(cumulative, .85), len(frequencies)-1)] / (rate / 2))
    bins = np.array_split(np.log(spectrum), 32)
    cepstral = dct(np.array([part.mean() for part in bins]), norm="ortho")[:13]
    _, _, power = spectrogram(values, fs=rate, nperseg=400, noverlap=240, mode="magnitude")
    log_power = np.log1p(power)
    frequency_bands = np.vstack([band.mean(axis=0) for band in np.array_split(log_power, 24, axis=0)])
    target_axis = np.linspace(0, 1, 16)
    source_axis = np.linspace(0, 1, frequency_bands.shape[1])
    time_frequency = np.concatenate([np.interp(target_axis, source_axis, band) for band in frequency_bands])
    duration = min(len(values) / rate / 5, 1.0)
    return np.array([rms, zcr, centroid, bandwidth, rolloff, duration, *cepstral, *time_frequency], dtype=float)


def wav_metrics(path: str | Path) -> dict[str, float | int]:
    rate, values = load_wav(path)
    features = audio_features(path)
    return {"sample_rate": rate, "samples": len(values), "duration_seconds": round(len(values)/rate, 3),
            "rms": round(float(features[0]), 4), "zero_crossing_rate": round(float(features[1]), 4)}


def write_tone(path: str | Path, frequency: float, seconds: float = 1.0, rate: int = 16000) -> Path:
    """Write a deterministic WAV fixture used only by dependency-light tests."""
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    times = np.arange(int(rate * seconds)) / rate
    envelope = np.minimum(1, times * 20) * np.minimum(1, (seconds - times) * 20)
    samples = (0.35 * np.sin(2*np.pi*frequency*times) * envelope * 32767).astype(np.int16)
    wavfile.write(target, rate, samples)
    return target


def chunk_wav(path: str | Path, seconds: float = 3.0) -> list[np.ndarray]:
    rate, values = load_wav(path)
    size = max(1, int(rate * seconds))
    return [values[index:index+size] for index in range(0, len(values), size) if len(values[index:index+size])]


def save_pcm(path: str | Path, values: np.ndarray, rate: int = 16000) -> Path:
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    clipped = np.clip(values, -1, 1)
    wavfile.write(target, rate, (clipped * 32767).astype(np.int16))
    return target


def classify_dataset(files: Iterable[Path], labels: Iterable[str], seed: int = 42) -> dict:
    """Train/evaluate a compact Random Forest on audio features."""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import train_test_split
    files, labels = list(files), list(labels)
    features = np.vstack([audio_features(path) for path in files])
    unique, counts = np.unique(labels, return_counts=True)
    stratify = labels if counts.min() >= 2 else None
    x_train,x_test,y_train,y_test=train_test_split(features,labels,test_size=.25,random_state=seed,stratify=stratify)
    model=RandomForestClassifier(n_estimators=160,random_state=seed,class_weight="balanced",n_jobs=1)
    model.fit(x_train,y_train); predictions=model.predict(x_test)
    return {"model":model,"accuracy":round(float(accuracy_score(y_test,predictions)),4),
            "train_samples":len(y_train),"test_samples":len(y_test),"classes":list(unique),
            "confusion_matrix":confusion_matrix(y_test,predictions,labels=list(unique)).tolist(),
            "truth":list(y_test),"predictions":list(predictions)}
