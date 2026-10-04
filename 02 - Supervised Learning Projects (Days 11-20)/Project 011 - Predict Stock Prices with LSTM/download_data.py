"""Download and cache adjusted AAPL daily prices with yfinance."""
from pathlib import Path
import time
import yfinance as yf

DESTINATION = Path(__file__).with_name("data") / "AAPL.csv"

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
            raise RuntimeError("No AAPL price data was returned after three download attempts")
        if data.empty:
            raise RuntimeError("No AAPL price data was returned")
        if getattr(data.columns, "nlevels", 1) > 1:
            data.columns = data.columns.get_level_values(0)
        DESTINATION.parent.mkdir(exist_ok=True)
        data.to_csv(DESTINATION)
    return DESTINATION

if __name__ == "__main__":
    print(ensure_dataset())
