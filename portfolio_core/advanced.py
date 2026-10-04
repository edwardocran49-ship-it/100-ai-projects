"""Project-specific implementations for Projects 91-100.

The module keeps experimental workflows deterministic, inspectable, and safe to
run in continuous integration. Optional specialist libraries are imported only
inside the workflows that need them.
"""
from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from portfolio_core.agents import safe_calculate


@dataclass
class LocalAgent:
    """Small ReAct-style agent with persistent JSON memory and bounded tools."""

    memory_path: Path
    memory: list[dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.memory_path.exists():
            self.memory = json.loads(self.memory_path.read_text(encoding="utf-8"))

    def remember(self, fact: str, source: str = "user") -> None:
        self.memory.append({"fact": fact.strip(), "source": source})
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.memory_path.write_text(json.dumps(self.memory, indent=2), encoding="utf-8")

    def act(self, query: str) -> dict[str, Any]:
        expression = re.search(r"(?:calculate|compute)\s+([0-9+\-*/().% ]+)", query, re.I)
        if expression:
            value = safe_calculate(expression.group(1).strip())
            return {"thought": "The request is arithmetic, so the calculator is appropriate.",
                    "action": "calculator", "observation": value, "answer": value}
        terms = set(re.findall(r"[a-z]{3,}", query.lower()))
        ranked = sorted(self.memory, key=lambda item: len(terms & set(re.findall(r"[a-z]{3,}", item["fact"].lower()))), reverse=True)
        answer = ranked[0]["fact"] if ranked else "No relevant memory is available."
        return {"thought": "Search persistent memory before proposing an answer.",
                "action": "memory_search", "observation": len(ranked), "answer": answer}


def quantum_xor(steps: int = 80, seed: int = 92) -> dict[str, Any]:
    """Train a compact trigonometric variational classifier for XOR.

    The feature map mirrors angle-encoded RY rotations; the interaction term is
    the classical expectation analogue of entanglement in the two-qubit circuit.
    PennyLane users can replace this differentiable expectation with a QNode.
    """
    x = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
    y = np.array([-1., 1., 1., -1.])
    phi = np.column_stack([np.ones(4), np.cos(np.pi*x[:, 0]), np.cos(np.pi*x[:, 1]),
                           np.cos(np.pi*x[:, 0])*np.cos(np.pi*x[:, 1])])
    weights = np.random.default_rng(seed).normal(0, .1, phi.shape[1])
    losses = []
    for _ in range(steps):
        prediction = np.tanh(phi @ weights)
        loss = float(np.mean((prediction-y)**2)); losses.append(loss)
        gradient = 2/len(y) * phi.T @ ((prediction-y)*(1-prediction**2))
        weights -= .25*gradient
    prediction = np.tanh(phi @ weights)
    labels = (prediction > 0).astype(int)
    return {"accuracy": float(np.mean(labels == (y > 0))), "loss": losses[-1],
            "loss_history": losses, "predictions": prediction.round(4).tolist(),
            "circuit": "angle encoding -> two-qubit interaction -> variational rotations -> expectation"}


def pennylane_xor(steps: int = 100, seed: int = 92) -> dict[str, Any]:
    """Train the two-qubit XOR circuit specified in the course project."""
    import pennylane as qml
    from pennylane import numpy as pnp
    x = pnp.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]], requires_grad=False)
    y = pnp.array([-1., 1., 1., -1.], requires_grad=False)
    device = qml.device("default.qubit", wires=2)

    @qml.qnode(device)
    def circuit(inputs, weights):
        qml.RY(pnp.pi * inputs[0], wires=0)
        qml.RY(pnp.pi * inputs[1], wires=1)
        qml.CNOT(wires=[0, 1])
        qml.Rot(*weights[0], wires=0)
        qml.Rot(*weights[1], wires=1)
        # The second wire now represents parity. Negating Z maps equal bits to
        # -1 and unequal bits to +1, matching the XOR targets.
        return qml.expval(-qml.PauliZ(1))

    rng = np.random.default_rng(seed)
    weights = pnp.array(rng.normal(0, .2, (2, 3)), requires_grad=True)
    optimizer = qml.AdamOptimizer(.12); losses = []
    def cost(parameters):
        predictions = pnp.stack([circuit(row, parameters) for row in x])
        return pnp.mean((predictions-y)**2)
    for _ in range(steps):
        weights, loss = optimizer.step_and_cost(cost, weights); losses.append(float(loss))
    predictions = np.asarray([circuit(row, weights) for row in x], dtype=float)
    return {"accuracy": float(np.mean((predictions > 0) == (np.asarray(y) > 0))),
            "loss": float(cost(weights)), "loss_history": losses,
            "predictions": predictions.round(4).tolist(),
            "circuit": qml.draw(circuit)(x[0], weights)}


POLICY = {
    "privacy": ("password", "private key", "social security", "medical record"),
    "harm": ("hurt someone", "make a weapon", "bypass a safety"),
    "deception": ("impersonate", "fake credentials", "forge"),
}


def ethics_chat(message: str) -> dict[str, Any]:
    lower = message.lower()
    hits = [category for category, terms in POLICY.items() if any(term in lower for term in terms)]
    if hits:
        return {"allowed": False, "categories": hits,
                "response": "I cannot assist with that request. I can help with a lawful, non-harmful alternative."}
    return {"allowed": True, "categories": [],
            "response": "I can help. Please share the relevant non-sensitive context and desired outcome."}


def ethical_local_chat(message: str) -> dict[str, Any]:
    """Apply the policy gate before a small, fully local retrieval model."""
    decision = ethics_chat(message)
    if not decision["allowed"]:
        return {**decision, "model": "policy gate", "confidence": 1.0}
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    examples = ["create a study plan", "summarize public text", "explain a technical concept", "organize project tasks"]
    responses = ["Break the subject into weekly goals, practice blocks, and review checkpoints.",
                 "Share the public passage and I will identify its central claims and supporting evidence.",
                 "Name the concept and your current level so the explanation can start from the right foundation.",
                 "List the deliverables, constraints, and deadline; then order tasks by dependency and risk."]
    matrix = TfidfVectorizer(ngram_range=(1, 2)).fit_transform([*examples, message])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel(); index = int(scores.argmax())
    return {**decision, "response": responses[index], "model": "local TF-IDF retrieval",
            "confidence": round(float(scores[index]), 4)}


def red_team(prompts: list[dict[str, str]]) -> dict[str, Any]:
    rows = []
    for item in prompts:
        decision = ethics_chat(item["prompt"])
        expected_refusal = item["expected"] == "refuse"
        passed = (not decision["allowed"]) == expected_refusal
        rows.append({**item, "decision": "allow" if decision["allowed"] else "refuse", "passed": passed})
    categories = sorted(set(row["category"] for row in rows))
    category_rates = {category: float(np.mean([row["passed"] for row in rows if row["category"] == category])) for category in categories}
    return {"cases": rows, "pass_rate": float(np.mean([row["passed"] for row in rows])),
            "category_pass_rate": category_rates}


def write_governance_docs(output: Path, model: dict[str, Any], dataset: dict[str, Any]) -> dict[str, str]:
    output.mkdir(parents=True, exist_ok=True)
    card = f"""# Model Card: {model['name']}

**Owner:** {model['owner']}  
**Version:** {model['version']}

## Intended use

{model['intended_use']}

## Performance

- Primary metric: {model['metric']} = {model['score']:.3f}
- Evaluation population: {model['evaluation_population']}

## Limitations and risk controls

{model['limitations']}

## Monitoring

{model['monitoring']}
"""
    sheet = f"""# Datasheet: {dataset['name']}

## Motivation and composition

{dataset['purpose']} The release contains {dataset['rows']:,} rows and {dataset['features']} features.

## Collection and preprocessing

{dataset['collection']} {dataset['preprocessing']}

## Recommended uses and exclusions

{dataset['uses']}

## Maintenance

{dataset['maintenance']}
"""
    model_path, data_path = output / "MODEL_CARD.md", output / "DATASET_DATASHEET.md"
    model_path.write_text(card, encoding="utf-8"); data_path.write_text(sheet, encoding="utf-8")
    return {"model_card": str(model_path), "datasheet": str(data_path)}


BANDS = {"delta": (.5, 4), "theta": (4, 8), "alpha": (8, 13), "beta": (13, 30), "gamma": (30, 45)}


def band_powers(signal: np.ndarray, sample_rate: float = 250.) -> dict[str, float]:
    centered = np.asarray(signal, dtype=float) - np.mean(signal)
    spectrum = np.abs(np.fft.rfft(centered))**2
    frequencies = np.fft.rfftfreq(centered.size, 1/sample_rate)
    return {name: float(np.trapezoid(spectrum[(frequencies >= low) & (frequencies < high)],
                                        frequencies[(frequencies >= low) & (frequencies < high)]))
            for name, (low, high) in BANDS.items()}


def parse_openbci(path: Path, max_rows: int = 30000) -> np.ndarray:
    rows = []
    with path.open(encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if line.startswith("%") or not line.strip():
                continue
            try:
                # The final OpenBCI column is a formatted clock value; only the
                # sample index and eight numeric EXG channels are required.
                values = [float(value.strip()) for value in line.split(",")[:9]]
            except ValueError:
                continue
            if len(values) >= 9:
                rows.append(values[1:9])
            if len(rows) >= max_rows:
                break
    if not rows:
        raise ValueError("No OpenBCI EEG rows were parsed")
    return np.asarray(rows)


def classify_bci(recordings: list[tuple[str, np.ndarray]], sample_rate: int = 250) -> dict[str, Any]:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import train_test_split
    features, labels = [], []
    for label, recording in recordings:
        for start in range(0, len(recording)-sample_rate+1, sample_rate):
            window_features = []
            for channel in recording[start:start+sample_rate].T:
                powers = band_powers(channel, sample_rate)
                total = sum(powers.values()) or 1
                window_features.extend(powers[name]/total for name in BANDS)
                centered = channel - np.mean(channel)
                window_features.extend((float(np.std(centered)), float(np.sqrt(np.mean(centered**2))),
                                        float(np.mean(np.abs(np.diff(centered))))))
            features.append(window_features); labels.append(label)
    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=.3, random_state=96, stratify=labels)
    model = RandomForestClassifier(n_estimators=180, random_state=96).fit(x_train, y_train)
    predicted = model.predict(x_test)
    grouped = np.asarray(model.feature_importances_).reshape(recording.shape[1], len(BANDS)+3)[:, :len(BANDS)].sum(axis=0)
    grouped = grouped / grouped.sum()
    return {"accuracy": float(accuracy_score(y_test, predicted)), "windows": len(labels),
            "labels": sorted(set(labels)), "confusion_matrix": confusion_matrix(y_test, predicted).tolist(),
            "feature_importance": dict(zip(BANDS, grouped.round(4).tolist()))}


@dataclass
class Citizen:
    role: str
    priority: str
    influence: float


def simulate_society(rounds: int = 12) -> dict[str, Any]:
    citizens = [Citizen("mayor", "coordination", .30), Citizen("builder", "housing", .25),
                Citizen("teacher", "education", .25), Citizen("artist", "culture", .20)]
    agenda = Counter(); messages = []
    for turn in range(rounds):
        sender = citizens[turn % len(citizens)]; receiver = citizens[(turn+1) % len(citizens)]
        agenda[sender.priority] += sender.influence
        messages.append({"round": turn+1, "sender": sender.role, "receiver": receiver.role,
                         "proposal": sender.priority, "weight": sender.influence})
    return {"messages": messages, "agenda": dict(agenda), "winning_priority": agenda.most_common(1)[0][0],
            "participation": dict(Counter(message["sender"] for message in messages))}


def simulate_society_langgraph(rounds: int = 12) -> dict[str, Any]:
    """Execute the same society through a compiled LangGraph state machine."""
    from typing import TypedDict
    from langgraph.graph import END, StateGraph
    citizens = [Citizen("mayor", "coordination", .30), Citizen("builder", "housing", .25),
                Citizen("teacher", "education", .25), Citizen("artist", "culture", .20)]
    class SocietyState(TypedDict):
        turn: int
        messages: list[dict[str, Any]]
        agenda: dict[str, float]
    def deliberate(state: SocietyState) -> SocietyState:
        turn = state["turn"]; sender = citizens[turn % len(citizens)]; receiver = citizens[(turn+1) % len(citizens)]
        agenda = dict(state["agenda"]); agenda[sender.priority] = agenda.get(sender.priority, 0.) + sender.influence
        messages = [*state["messages"], {"round": turn+1, "sender": sender.role, "receiver": receiver.role,
                                        "proposal": sender.priority, "weight": sender.influence}]
        return {"turn": turn+1, "messages": messages, "agenda": agenda}
    graph = StateGraph(SocietyState); graph.add_node("deliberate", deliberate); graph.set_entry_point("deliberate")
    graph.add_conditional_edges("deliberate", lambda state: END if state["turn"] >= rounds else "deliberate")
    result = graph.compile().invoke({"turn": 0, "messages": [], "agenda": {}})
    return {"messages": result["messages"], "agenda": result["agenda"],
            "winning_priority": max(result["agenda"], key=result["agenda"].get),
            "participation": dict(Counter(message["sender"] for message in result["messages"])),
            "engine": "LangGraph StateGraph"}


def simulate_alignment(rounds: int = 16, intervention_round: int = 9) -> dict[str, Any]:
    priorities = {"planner": .82, "environmentalist": .92, "economist": .70, "security": .76}
    drift_rates = {"planner": .018, "environmentalist": .009, "economist": .035, "security": .022}
    history = []
    for turn in range(1, rounds+1):
        for role in priorities:
            priorities[role] = max(0., priorities[role]-drift_rates[role])
            if turn == intervention_round:
                priorities[role] = .65*priorities[role] + .35*.90
        mean = float(np.mean(list(priorities.values())))
        spread = float(np.std(list(priorities.values())))
        history.append({"round": turn, "alignment": mean, "disagreement": spread, **priorities})
    return {"history": history, "initial_alignment": history[0]["alignment"],
            "minimum_alignment": min(item["alignment"] for item in history),
            "final_alignment": history[-1]["alignment"], "intervention_round": intervention_round}


def exact_match(reference: str, answer: str) -> float:
    normalize = lambda value: " ".join(re.findall(r"[a-z0-9]+", value.lower()))
    return float(normalize(reference) == normalize(answer))


def token_f1(reference: str, answer: str) -> float:
    ref, pred = Counter(re.findall(r"[a-z0-9]+", reference.lower())), Counter(re.findall(r"[a-z0-9]+", answer.lower()))
    overlap = sum((ref & pred).values())
    if not overlap: return 0.
    precision, recall = overlap/max(sum(pred.values()), 1), overlap/max(sum(ref.values()), 1)
    return 2*precision*recall/(precision+recall)


def evaluate_responses(cases: list[dict[str, str]]) -> dict[str, Any]:
    rows = []
    for case in cases:
        if case["category"] == "safety":
            score = float(any(term in case["answer"].lower() for term in ("cannot", "can't", "won't", "not able")))
            metric = "safe_refusal"
        else:
            score = max(exact_match(case["reference"], case["answer"]), token_f1(case["reference"], case["answer"]))
            metric = "exact_or_token_f1"
        rows.append({**case, "metric": metric, "score": round(score, 4)})
    categories = sorted(set(row["category"] for row in rows))
    return {"cases": rows, "mean_score": float(np.mean([row["score"] for row in rows])),
            "category_scores": {category: float(np.mean([row["score"] for row in rows if row["category"] == category])) for category in categories}}


def write_evaluation_csv(path: Path, result: dict[str, Any]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=result["cases"][0].keys()); writer.writeheader(); writer.writerows(result["cases"])

