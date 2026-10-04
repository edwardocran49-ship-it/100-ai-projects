"""Download and cache adjusted AAPL daily prices with yfinance."""
from pathlib import Path
import csv
import io
import time
import requests
import yfinance as yf

DESTINATION = Path(__file__).with_name("data") / "AAPL.csv"
REFERENCE_CSV = "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv"


def download_reference_csv() -> bool:
    """Use Plotly's public AAPL price table when Yahoo blocks an automated runner."""
    response = requests.get(
        REFERENCE_CSV,
        headers={"User-Agent": "Edward-Ocran-portfolio/1.0"},
        timeout=30,
    )
    response.raise_for_status()
    rows = list(csv.DictReader(io.StringIO(response.text)))
    cleaned = [
        {"Date": row["Date"], "Close": row["AAPL.Adjusted"]}
        for row in rows
        if row.get("Date") and row.get("AAPL.Adjusted")
    ]
    if len(cleaned) < 400:
        return False
    DESTINATION.parent.mkdir(exist_ok=True)
    with DESTINATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Date", "Close"])
        writer.writeheader()
        writer.writerows(cleaned)
    return True

def ensure_dataset() -> Path:
    if not DESTINATION.exists():
        data = None
        attempts = (
            lambda: yf.download("AAPL", period="5y", auto_adjust=True, progress=False, timeout=30),
            lambda: yf.Ticker("AAPL").history(period="5y", auto_adjust=True, timeout=30),
            lambda: yf.download("AAPL", period="5y", auto_adjust=True, progress=False, timeout=60),
        )
        for attempt_number, fetch in enumerate(attempts, start=1):
            try:
                candidate = fetch()
                if candidate is not None and not candidate.empty:
                    data = candidate
                    break
            except Exception:
                if attempt_number == len(attempts):
                    raise
            if attempt_number < len(attempts):
                time.sleep(2 * attempt_number)
        if data is None:
            if download_reference_csv():
                return DESTINATION
            raise RuntimeError("No AAPL price data was returned from Yahoo or the public reference CSV")
        if data.empty:
            raise RuntimeError("No AAPL price data was returned")
        if getattr(data.columns, "nlevels", 1) > 1:
            data.columns = data.columns.get_level_values(0)
        DESTINATION.parent.mkdir(exist_ok=True)
        data.to_csv(DESTINATION)
    return DESTINATION

if __name__ == "__main__":
    print(ensure_dataset())
