# Project 45: License Plate Detection

**Author:** Edward Ocran

Find plate-shaped regions with OpenCV edges and contours, then read the leading crop with EasyOCR. The normal run uses `Cars379.png` from the Kaggle Car Plate Detection dataset.

## Run

```powershell
pip install -r requirements.txt
python download_data.py
python main.py
python -m unittest -v test_project.py
```

Data notes: [INPUT.md](INPUT.md)  
Findings: [Analysis report](ANALYSIS_REPORT.md)
