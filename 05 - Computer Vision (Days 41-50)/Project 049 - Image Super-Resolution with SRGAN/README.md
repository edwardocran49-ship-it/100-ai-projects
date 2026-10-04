# Project 49: Image Super-Resolution with SRGAN

**Author:** Edward Ocran

Upscale a 64 × 64 photograph to 256 × 256 with pretrained Real-ESRGAN x4plus and compare it with bicubic interpolation using PSNR and visual evidence.

## Run

```powershell
pip install -r requirements.txt
python main.py
python -m unittest -v test_project.py
```

Output: `outputs/super_resolved.png`  
Findings: [Analysis report](ANALYSIS_REPORT.md)
