# Portfolio Evidence and Validation Standards

**Author:** Edward Ocran

## Documentation names

- `DATASET.md` documents a dataset or recorded corpus: source, retrieval, local location, coverage, and licensing or access conditions.
- `INPUTS.md` documents source documents, webpages, prompts, evaluation fixtures, service requests, or user-supplied media that are not training datasets.
- `ANALYSIS_REPORT.md` remains the stable report filename across the portfolio. The report heading states its actual purpose rather than forcing every project into a data-analysis format.

## Validation levels

### Dependency-light smoke validation

Confirms that the project entry point runs, returns the expected JSON contract, and exercises its core behavior with bounded local inputs. This is the level used by the repository-wide GitHub Actions workflow.

### Source-backed or representative-input run

Runs the substantive workflow against the documented dataset, public source, recording, document, or representative input. Analytical claims and charts must come from this level or a stronger one—not from a smoke fixture.

### Full framework run

Runs the framework named in the project brief, such as PennyLane or LangGraph, with the project's normal execution path. A separate smoke path may remain for portable continuous integration.

### Environment-dependent validation

Requires a live service, browser permission, microphone, hardware device, large local model, deployment account, or container runtime. Offline tests may verify the core, but they do not establish that the environment-dependent integration is operational.

## Reporting rules

- Data projects report source, sample size, preparation, evaluation design, metrics, limitations, and charts calculated from the documented run.
- Agent projects report tool routing, task success, safety boundaries, memory behavior, and failure cases.
- Deployment projects report application-core behavior, request validation, packaging, privacy boundaries, and remaining live-environment checks.
- Safety and governance projects report evaluation-set coverage, policy outcomes, documentation completeness, and unresolved risks.
- Simulation projects separate assumptions from observations and avoid treating modeled scenarios as real-world evidence.
- Reflection projects use the authored document as the primary deliverable; any report is supplementary.

## Claims policy

A green smoke workflow means all 100 entry points passed their portable checks. It is not evidence that every external dataset was downloaded again or that every external service, microphone, hardware device, large model, and deployment target was exercised. Project-level claims must match the strongest validation actually completed and documented in the [verification matrix](PROJECT_VERIFICATION.md).
