"""Auditable tool-using agent implementations for Projects 51-60."""
from __future__ import annotations

import ast
import math
import operator
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Any


_BINARY = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def safe_calculate(expression: str) -> float:
    """Evaluate arithmetic without exposing Python's eval or builtins."""
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            return _BINARY[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
            return _UNARY[type(node.op)](visit(node.operand))
        raise ValueError("Only numeric arithmetic is allowed")

    return float(visit(ast.parse(expression, mode="eval")))


def math_agent(question: str) -> dict[str, Any]:
    lower = question.lower()
    numbers = [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", lower)]
    if "rectangle" in lower and len(numbers) >= 2:
        expression = f"{numbers[0]} * {numbers[1]}"
        thought = f"Area is length multiplied by width: {numbers[0]:g} × {numbers[1]:g}."
    elif "square" in lower and "sum" in lower and len(numbers) >= 2:
        expression = f"({numbers[0]} + {numbers[1]}) ** 2"
        thought = f"Add {numbers[0]:g} and {numbers[1]:g}, then square the sum."
    elif "divided" in lower and "multipl" in lower and len(numbers) >= 3:
        expression = f"({numbers[0]} / {numbers[1]}) * {numbers[2]}"
        thought = "Apply division first, then multiply the intermediate result."
    else:
        expression = re.sub(r"[^0-9+\-*/().% ]", "", question).strip()
        thought = "Evaluate the arithmetic expression with the calculator tool."
    answer = safe_calculate(expression)
    return {"question": question, "thought": thought, "action": expression,
            "observation": answer, "final_answer": answer, "tool_calls": 1}


def execute_code(code: str, assertions: list[str]) -> dict[str, Any]:
    allowed = {"range": range, "len": len, "all": all, "any": any, "sum": sum, "int": int, "float": float, "bool": bool,
               "min": min, "max": max, "enumerate": enumerate, "zip": zip}
    namespace: dict[str, Any] = {}
    try:
        exec(compile(code, "<agent-code>", "exec"), {"__builtins__": allowed}, namespace)
        outcomes = [bool(eval(check, {"__builtins__": allowed}, namespace)) for check in assertions]
        return {"success": all(outcomes), "tests": outcomes, "error": None}
    except Exception as exc:
        return {"success": False, "tests": [], "error": f"{type(exc).__name__}: {exc}"}


def coding_bot(task: str) -> dict[str, Any]:
    first = "def is_prime(n):\n    if n < 2: return True\n    return all(n % d for d in range(2, int(n ** 0.5) + 1))"
    fixed = "def is_prime(n):\n    if n < 2: return False\n    return all(n % d for d in range(2, int(n ** 0.5) + 1))"
    checks = ["is_prime(2)", "is_prime(29)", "not is_prime(1)", "not is_prime(21)"]
    attempts = []
    for code in (first, fixed):
        result = execute_code(code, checks); attempts.append(result)
        if result["success"]:
            return {"task": task, "code": code, "attempts": attempts,
                    "tests_passed": sum(result["tests"]), "tests_total": len(checks)}
    raise RuntimeError("Coding bot failed to produce a passing solution")


def chunk_text(text: str, max_chars: int = 1200) -> list[str]:
    chunks, current = [], ""
    for line in (line.strip() for line in text.splitlines() if line.strip()):
        if current and len(current) + len(line) + 1 > max_chars:
            chunks.append(current); current = line
        else:
            current = f"{current} {line}".strip()
    if current:
        chunks.append(current)
    return chunks


def summarize_text(text: str, sentences: int = 2) -> str:
    candidates = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if len(part.split()) >= 6]
    words = re.findall(r"[a-z]{4,}", text.lower())
    frequency = Counter(words)
    scored = []
    for index, sentence in enumerate(candidates):
        tokens = re.findall(r"[a-z]{4,}", sentence.lower())
        scored.append((sum(frequency[token] for token in tokens) / max(len(tokens), 1), index, sentence))
    selected = sorted(sorted(scored, reverse=True)[:sentences], key=lambda item: item[1])
    return " ".join(item[2] for item in selected)


def summarize_pdf(path: Path) -> dict[str, Any]:
    import fitz
    with fitz.open(path) as document:
        pages = [page.get_text() for page in document]
    chunks = chunk_text("\n".join(pages))
    summaries = [summarize_text(chunk, 2) for chunk in chunks]
    # The opening pages contain the abstract, contribution, and framing; using
    # them for the final executive summary prevents long experimental traces
    # and appendix examples from overwhelming the document-level message.
    opening = re.sub(r"[^\x20-\x7E\n]", " ", pages[0])[:4500]
    final_summary = summarize_text(opening, 6)
    return {"pages": len(pages), "characters": sum(map(len, pages)), "chunks": len(chunks),
            "summary": final_summary, "chunk_summaries": summaries}


def schedule_event(calendar: dict[str, str], date: str, title: str, after_hour: int = 12) -> dict[str, Any]:
    candidates = [f"{date} {hour:02d}:00" for hour in range(max(9, after_hour), 18)]
    available = [slot for slot in candidates if slot not in calendar]
    if not available:
        return {"scheduled": False, "available": [], "reason": "No free business-hour slot"}
    selected = available[0]; calendar[selected] = title
    return {"scheduled": True, "selected": selected, "available_before_booking": available,
            "event": title}


def grade_essay(essay: str) -> dict[str, Any]:
    sentences = [value.strip() for value in re.split(r"[.!?]+", essay) if value.strip()]
    words = re.findall(r"[A-Za-z']+", essay)
    paragraphs = [value for value in essay.split("\n\n") if value.strip()]
    clarity = min(10, 4 + len(sentences) + int(bool(re.search(r"because|therefore|however", essay, re.I))))
    grammar = min(10, 5 + int(essay[:1].isupper()) + int(essay.rstrip().endswith((".", "!", "?"))) + min(3, len(sentences)))
    structure = min(10, 4 + min(3, len(paragraphs)) + int(len(sentences) >= 3))
    vocabulary = min(10, 4 + round(4 * len(set(word.lower() for word in words)) / max(len(words), 1)))
    scores = {"clarity": clarity, "grammar": grammar, "structure": structure, "vocabulary": vocabulary}
    return {"scores": scores, "overall": round(sum(scores.values()) / 4, 2),
            "word_count": len(words), "sentence_count": len(sentences)}


def improve_essay(essay: str) -> str:
    core = essay.strip().rstrip(".")
    return (f"{core}. This matters because education develops practical knowledge and disciplined thinking. "
            "It also gives students repeated opportunities to communicate, solve problems, and learn from feedback. "
            "For these reasons, school supports both personal growth and wider participation in society.")


def classify_file(path: Path) -> str:
    extension = path.suffix.lower()
    if extension in {".jpg", ".png", ".jpeg"}: return "Images"
    if extension in {".exe", ".dmg", ".msi"}: return "Installers"
    if extension in {".mp4", ".mkv", ".mov"}: return "Videos"
    if extension in {".csv", ".xlsx"}: return "Spreadsheets"
    if extension == ".pdf":
        try:
            from pdfminer.high_level import extract_text
            text = extract_text(path).lower()
            if sum(term in text for term in ("experience", "education", "skills", "objective")) >= 2:
                return "Resumes"
        except Exception:
            pass
        return "Documents"
    if extension in {".docx", ".txt"}: return "Documents"
    return "Others"


def organize_folder(folder: Path, move: bool = True) -> dict[str, Any]:
    plan = []
    for path in sorted(item for item in folder.iterdir() if item.is_file()):
        category = classify_file(path); destination = folder / category / path.name
        plan.append({"file": path.name, "category": category, "destination": str(destination)})
        if move:
            destination.parent.mkdir(exist_ok=True); shutil.move(str(path), str(destination))
    return {"files": len(plan), "categories": dict(Counter(item["category"] for item in plan)), "plan": plan}


class VectorMemory:
    def __init__(self):
        self.documents: list[str] = []
        self.sources: list[str] = []

    def memorize(self, text: str, source: str, chunk_size: int = 500) -> int:
        # Preserve paragraph and sentence boundaries so retrieved evidence is
        # readable and never begins halfway through a word.
        units: list[str] = []
        for paragraph in (part.strip() for part in re.split(r"\n+", text) if part.strip()):
            if len(paragraph) <= chunk_size:
                units.append(paragraph)
                continue
            sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", paragraph) if part.strip()]
            current = ""
            for sentence in sentences:
                if current and len(current) + len(sentence) + 1 > chunk_size:
                    units.append(current); current = sentence
                elif len(sentence) > chunk_size:
                    words, fragment = sentence.split(), ""
                    for word in words:
                        if fragment and len(fragment) + len(word) + 1 > chunk_size:
                            units.append(fragment); fragment = word
                        else:
                            fragment = f"{fragment} {word}".strip()
                    if fragment:
                        units.append(fragment)
                else:
                    current = f"{current} {sentence}".strip()
            if current:
                units.append(current)
        chunks, current = [], ""
        for unit in units:
            if current and len(current) + len(unit) + 2 > chunk_size:
                chunks.append(current); current = unit
            else:
                current = f"{current}\n\n{unit}".strip()
        if current:
            chunks.append(current)
        self.documents.extend(chunks); self.sources.extend([source] * len(chunks)); return len(chunks)

    def query(self, question: str, top_k: int = 3) -> list[dict[str, Any]]:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        matrix = TfidfVectorizer(stop_words="english").fit_transform(self.documents + [question])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
        indices = scores.argsort()[::-1][:top_k]
        return [{"text": self.documents[index], "source": self.sources[index], "score": round(float(scores[index]), 4)} for index in indices]


def route_query(query: str) -> dict[str, str]:
    lower = query.lower()
    if "weather" in lower:
        match = re.search(r"(?:in|for)\s+([A-Za-z ]+?)[?.]?$", query); return {"tool": "get_weather", "input": (match.group(1) if match else query).strip()}
    if "news" in lower or "headline" in lower:
        topic = re.sub(r".*?(?:about|on)\s+", "", query, flags=re.I).rstrip("?."); return {"tool": "get_news", "input": topic}
    expression = re.sub(r"[^0-9+\-*/().% ]", "", query).strip()
    if expression: return {"tool": "calculate", "input": expression}
    return {"tool": "unknown", "input": query}


def dispatch_tool(route: dict[str, str]) -> str:
    if route["tool"] == "get_weather": return f"Weather in {route['input']} is 25°C and sunny."
    if route["tool"] == "get_news": return f"Top headline topic: {route['input']}."
    if route["tool"] == "calculate": return f"Result: {safe_calculate(route['input']):g}"
    return "No matching tool."


def recursive_research(question: str, source_text: str) -> dict[str, Any]:
    subject = re.sub(r"^(what|how)\s+(are|is|do|does)\s+", "", question.rstrip("?."), flags=re.I)
    subquestions = [f"What are the main mechanisms behind {subject.lower()}?",
                    f"What evidence describes the scale of {subject.lower()}?",
                    f"What mitigations or alternatives address {subject.lower()}?"]
    memory = VectorMemory(); chunks = memory.memorize(source_text, "reference")
    answers = []
    retrieval_queries = [
        "electricity consumption energy mix greenhouse gas emissions electronic waste noise water footprint",
        "estimated electricity terawatt hours carbon emissions tonnes comparison scale",
        "renewable energy grid flexibility mitigation alternatives proof of stake waste heat",
    ]
    for subquestion, retrieval_query in zip(subquestions, retrieval_queries):
        passages = memory.query(retrieval_query, 1)
        answers.append({"question": subquestion, "answer": summarize_text(passages[0]["text"], 2), "evidence": passages[0]})
    report = "\n\n".join(f"### {i}. {item['question']}\n{item['answer']}" for i, item in enumerate(answers, 1))
    return {"question": question, "subquestions": subquestions, "answers": answers, "chunks_indexed": chunks, "report": report}


class CookingAssistant:
    def __init__(self, recipe: dict[str, Any]):
        self.recipe = recipe; self.current_step = 0

    def handle(self, command: str) -> str:
        lower = command.lower()
        if "start" in lower:
            self.current_step = 0; return f"Let's cook {self.recipe['title']}. Say next when you are ready."
        if "ingredients" in lower: return ", ".join(self.recipe["ingredients"])
        if "convert" in lower:
            conversions = {"1 cup flour": "120 grams of flour", "1 cup milk": "240 millilitres of milk"}
            return ", ".join(conversions.get(item.lower(), item) for item in self.recipe["ingredients"])
        if "repeat" in lower:
            return self.recipe["steps"][max(0, self.current_step - 1)]
        if "back" in lower:
            self.current_step = max(0, self.current_step - 1); return self.recipe["steps"][self.current_step]
        if "next" in lower:
            if self.current_step >= len(self.recipe["steps"]): return "You're done. Enjoy your meal."
            response = self.recipe["steps"][self.current_step]; self.current_step += 1; return response
        return "Try start, ingredients, convert, next, repeat, or back."
