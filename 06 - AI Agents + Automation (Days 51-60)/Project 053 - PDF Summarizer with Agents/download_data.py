"""Download the public ReAct paper used for the PDF summarization run."""
from pathlib import Path
from urllib.request import urlretrieve
URL = "https://arxiv.org/pdf/2210.03629"


def ensure_document() -> Path:
    target = Path(__file__).resolve().parent / "data" / "react-paper.pdf"
    target.parent.mkdir(exist_ok=True)
    if not target.exists(): urlretrieve(URL, target)
    return target
if __name__ == "__main__": print(ensure_document())
