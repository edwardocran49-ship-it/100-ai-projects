# Project 46: OCR for Handwritten Notes

**Author:** Edward Ocran

Detect and transcribe a genuine handwritten English line with EasyOCR, then compare the output with the IAM reference transcription using character and word error rates.

## Run

```powershell
pip install -r requirements.txt
python download_data.py
python main.py
python -m unittest -v test_project.py
```

Data notes: [INPUT.md](INPUT.md)  
Findings: [Analysis report](ANALYSIS_REPORT.md)

## Inputs

See [INPUTS.md](INPUTS.md) for the input type, evaluation fixtures, and privacy boundary.
