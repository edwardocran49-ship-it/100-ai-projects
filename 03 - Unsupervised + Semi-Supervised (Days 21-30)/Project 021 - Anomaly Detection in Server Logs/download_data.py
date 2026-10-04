from pathlib import Path
import requests

CACHE = Path.home() / ".cache" / "project21-nab"
SERIES = CACHE / "ec2_cpu_utilization_5f5533.csv"
LABELS = CACHE / "combined_windows.json"

def ensure_dataset():
    CACHE.mkdir(parents=True, exist_ok=True)
    urls = {
        SERIES: "https://raw.githubusercontent.com/numenta/NAB/master/data/realAWSCloudwatch/ec2_cpu_utilization_5f5533.csv",
        LABELS: "https://raw.githubusercontent.com/numenta/NAB/master/labels/combined_windows.json",
    }
    for path, url in urls.items():
        if not path.exists():
            response = requests.get(url, timeout=60); response.raise_for_status(); path.write_bytes(response.content)
    return SERIES, LABELS
