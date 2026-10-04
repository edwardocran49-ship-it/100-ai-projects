# Project 55: Self-Correcting Essay Grader

**Author:** Edward Ocran  
**Category:** AI Agents + Automation (Days 51–60)

## Objective

Grade an essay against a rubric, revise it, and measure the change.

## Included

- `main.py` — runnable implementation of the course workflow.
- `test_project.py` — project-specific behavior checks.
- `ANALYSIS_REPORT.md` — technical evaluation with two rendered figures.
- `analysis_assets/` — report figures generated from the validated run.

## Run

```powershell
pip install -r requirements.txt
python main.py
python -m unittest -v test_project.py
```

## Result

The checked demonstration passes its behavioral tests. See [the analysis report](ANALYSIS_REPORT.md) for the observed metrics, interpretation, and limitations.

The course PDF is not redistributed in this public repository.

## Inputs

See [INPUTS.md](INPUTS.md) for the input type, evaluation fixtures, and privacy boundary.
