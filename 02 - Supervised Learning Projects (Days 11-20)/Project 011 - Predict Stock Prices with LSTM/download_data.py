"""Download and cache adjusted AAPL daily prices with yfinance."""
from pathlib import Path
import yfinance as yf

DESTINATION = Path(__file__).with_name("data") / "AAPL.csv"

def ensure_dataset() -> Path:
    if not DESTINATION.exists():
        data = yf.download("AAPL", period="5y", auto_adjust=True, progress=False)
        if data.empty:
            raise RuntimeError("No AAPL price data was returned")
        if getattr(data.columns, "nlevels", 1) > 1:
            data.columns = data.columns.get_level_values(0)
        DESTINATION.parent.mkdir(exist_ok=True)
        data.to_csv(DESTINATION)
    return DESTINATION

if __name__ == "__main__":
    print(ensure_dataset())
