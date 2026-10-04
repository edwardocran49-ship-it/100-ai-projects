# Project 84: Create a Hugging Face Space

**Author:** Edward Ocran

## Objective

Implement and validate the course deployment workflow for create a hugging face space.

## Included

- `main.py` — testable application core.
- `test_project.py` — automated behavior check.
- `ANALYSIS_REPORT.md` — deployment validation with two figures.
- `analysis_assets/` — report figures.
- `INPUTS.md` — fixtures, reference inputs, and privacy notes.

## Run

```powershell
pip install -r requirements.txt
python main.py --json
python -m unittest -v test_project.py
```

Web-specific entry files such as `app.py` or `Dockerfile` are included where required. The course PDF is not redistributed.
