"""NLP implementations used by Projects 31-40.

Large pretrained models are loaded lazily so importing a project remains fast.
Public functions accept an optional backend for focused unit testing without
changing the production execution path.
"""
from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any, Callable, Iterable


def pipeline_backend(task: str, model: str):
    from transformers import pipeline

    return pipeline(task, model=model, framework="pt")


def classify_sentiment(
    texts: list[str],
    backend: Callable[[list[str]], list[dict[str, Any]]] | None = None,
) -> list[dict[str, Any]]:
    predictor = backend or pipeline_backend(
        "sentiment-analysis", "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    )
    try:
        raw = predictor(texts, truncation=True)
    except TypeError:
        # Simple injected test backends may only accept the text batch.
        raw = predictor(texts)
    return [
        {
            "text": text,
            "label": str(item["label"]).lower().replace("label_1", "positive").replace("label_0", "negative"),
            "confidence": round(float(item["score"]), 4),
        }
        for text, item in zip(texts, raw)
    ]


def evaluate_sentiment(
    records: Iterable[dict[str, Any]],
    backend: Callable[[list[str]], list[dict[str, Any]]] | None = None,
    batch_size: int = 32,
) -> dict[str, Any]:
    """Evaluate the BERT classifier against labelled review records."""
    from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support

    rows = list(records)
    texts = [str(row["text"]) for row in rows]
    expected = [int(row["label"]) for row in rows]
    predicted: list[int] = []
    predictor = backend or pipeline_backend(
        "sentiment-analysis", "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    )
    for start in range(0, len(texts), batch_size):
        results = classify_sentiment(texts[start:start + batch_size], backend=predictor)
        predicted.extend(1 if item["label"] == "positive" else 0 for item in results)
    precision, recall, f1, _ = precision_recall_fscore_support(
        expected, predicted, average="binary", zero_division=0
    )
    tn, fp, fn, tp = confusion_matrix(expected, predicted, labels=[0, 1]).ravel()
    return {
        "records": len(rows),
        "accuracy": round(float(accuracy_score(expected, predicted)), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1": round(float(f1), 4),
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
    }


def summarize_text(
    text: str,
    backend: Callable[..., list[dict[str, str]]] | None = None,
) -> str:
    summarizer = backend or pipeline_backend("summarization", "google-t5/t5-small")
    result = summarizer(text, max_new_tokens=60, min_length=15, do_sample=False)
    return str(result[0]["summary_text"]).strip()


def answer_question(
    question: str,
    context: str,
    backend: Callable[..., dict[str, Any]] | None = None,
) -> dict[str, Any]:
    reader = backend or pipeline_backend(
        "question-answering", "distilbert/distilbert-base-cased-distilled-squad"
    )
    result = reader(question=question, context=context)
    return {
        "answer": str(result["answer"]),
        "score": round(float(result["score"]), 4),
        "start": int(result.get("start", -1)),
        "end": int(result.get("end", -1)),
    }


def train_spam_classifier(csv_path: Path) -> dict[str, Any]:
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import make_pipeline

    frame = pd.read_csv(csv_path, encoding="latin-1")[["v1", "v2"]].dropna()
    X_train, X_test, y_train, y_test = train_test_split(
        frame.v2, frame.v1, test_size=.2, random_state=42, stratify=frame.v1
    )
    model = make_pipeline(TfidfVectorizer(stop_words="english"), MultinomialNB())
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, predicted, average="binary", pos_label="spam", zero_division=0
    )
    tn, fp, fn, tp = confusion_matrix(y_test, predicted, labels=["ham", "spam"]).ravel()
    return {
        "model": model,
        "records": len(frame),
        "metrics": {
            "accuracy": round(float(accuracy_score(y_test, predicted)), 4),
            "spam_precision": round(float(precision), 4),
            "spam_recall": round(float(recall), 4),
            "spam_f1": round(float(f1), 4),
            "true_negative": int(tn),
            "false_positive": int(fp),
            "false_negative": int(fn),
            "true_positive": int(tp),
        },
    }


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s().-]{7,}\d")
DEFAULT_SKILLS = {
    "python", "java", "sql", "excel", "aws", "tensorflow", "pytorch",
    "tableau", "power bi", "machine learning", "data analysis",
}


def load_resume_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        import pdfplumber

        with pdfplumber.open(path) as document:
            return "\n".join(page.extract_text() or "" for page in document.pages).strip()
    return path.read_text(encoding="utf-8")


def _spacy_model():
    import spacy

    return spacy.load("en_core_web_sm")


def _section(text: str, heading: str, stop_headings: Iterable[str]) -> str:
    lines = text.splitlines()
    start = next((i + 1 for i, line in enumerate(lines) if line.strip().lower() == heading.lower()), None)
    if start is None:
        return ""
    stops = {item.lower() for item in stop_headings}
    collected = []
    for line in lines[start:]:
        if line.strip().lower() in stops:
            break
        if line.strip():
            collected.append(line.strip())
    return " ".join(collected)


def parse_resume(text: str, nlp=None) -> dict[str, Any]:
    doc = (nlp or _spacy_model())(text)
    name = next((entity.text for entity in doc.ents if entity.label_ == "PERSON"), None)
    email = EMAIL_RE.search(text)
    phone = PHONE_RE.search(text)
    lowered = text.lower()
    headings = ("education", "experience", "skills", "projects", "certifications")
    return {
        "name": name,
        "email": email.group(0) if email else None,
        "phone": phone.group(0).strip() if phone else None,
        "skills": sorted(skill for skill in DEFAULT_SKILLS if skill in lowered),
        "education": _section(text, "education", headings),
        "experience": _section(text, "experience", headings),
    }


def extract_entities(text: str, nlp=None) -> list[dict[str, Any]]:
    doc = (nlp or _spacy_model())(text)
    return [
        {"text": entity.text, "label": entity.label_, "start": entity.start_char, "end": entity.end_char}
        for entity in doc.ents
    ]


def semantic_search(
    query: str,
    documents: list[str],
    encoder: Callable[[list[str]], Any] | None = None,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    import numpy as np

    if encoder is None:
        import os
        os.environ.setdefault("USE_TF", "0")
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        encoder = lambda values: model.encode(values, normalize_embeddings=True)
    document_vectors = np.asarray(encoder(documents), dtype=float)
    query_vector = np.asarray(encoder([query])[0], dtype=float)
    document_vectors /= np.linalg.norm(document_vectors, axis=1, keepdims=True).clip(min=1e-12)
    query_vector /= max(np.linalg.norm(query_vector), 1e-12)
    scores = document_vectors @ query_vector
    order = np.argsort(scores)[::-1][:top_k]
    return [
        {"rank": rank, "document": documents[index], "score": round(float(scores[index]), 4)}
        for rank, index in enumerate(order, start=1)
    ]


def zero_shot_classify(
    text: str,
    labels: list[str],
    backend: Callable[..., dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    classifier = backend or pipeline_backend("zero-shot-classification", "facebook/bart-large-mnli")
    result = classifier(text, candidate_labels=labels, multi_label=False)
    return [
        {"label": str(label), "score": round(float(score), 4)}
        for label, score in zip(result["labels"], result["scores"])
    ]


def dialog_reply(
    message: str,
    history: list[tuple[str, str]] | None = None,
    backend: Callable[..., str] | None = None,
) -> str:
    if backend is not None:
        return str(backend(message=message, history=history or [])).strip()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
    prior = "".join(f"{user}{tokenizer.eos_token}{bot}{tokenizer.eos_token}" for user, bot in history or [])
    encoded = tokenizer(prior + message + tokenizer.eos_token, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            input_ids=encoded["input_ids"], attention_mask=encoded["attention_mask"],
            max_new_tokens=80, pad_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(output[0, encoded["input_ids"].shape[-1]:], skip_special_tokens=True).strip()


def translate_text(
    text: str,
    backend: Callable[[str], list[dict[str, str]]] | None = None,
) -> str:
    translator = backend or pipeline_backend("translation", "Helsinki-NLP/opus-mt-en-fr")
    return str(translator(text)[0]["translation_text"]).strip()


def token_overlap(reference: str, candidate: str) -> float:
    expected = set(re.findall(r"\w+", reference.lower()))
    observed = set(re.findall(r"\w+", candidate.lower()))
    return 0.0 if not expected else len(expected & observed) / len(expected)
