# Project 50: Satellite Image Segmentation

**Author:** Edward Ocran

Encode DeepGlobe land-cover masks and train a compact UNet-style encoder-decoder on real satellite image/mask pairs.

## Run

```powershell
pip install -r requirements.txt
python download_data.py
python main.py
python -m unittest -v test_project.py
```

Dataset provenance: [DATASET.md](DATASET.md)  
Findings: [Analysis report](ANALYSIS_REPORT.md)
