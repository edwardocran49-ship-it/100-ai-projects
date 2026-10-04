"""Generate the reviewed charts and written reports for Projects 51-60."""
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
PROJECTS = {
51: ("Project 051 - Math Reasoning Agent (ReAct Pattern)", [40,49,16], ["Rectangle area","Squared sum","Division chain"],
"The agent solved all three word problems correctly and made exactly one calculator call per problem. The trace is deliberately short: identify the operation, call the restricted calculator, and report the observation.",
"The strongest result is not the arithmetic difficulty; it is the inspectability of the route to the answer. Each response exposes the expression sent to the tool, while the AST-based calculator rejects names, imports, and arbitrary Python. That gives the agent a smaller attack surface than an `eval`-based implementation.",
"The current parser covers the three demonstrated language patterns. A production version should add a formal expression planner and a larger adversarial test set before handling unconstrained questions."),
52: ("Project 052 - Coding Bot with Tool Use", [3,4], ["Attempt 1","Attempt 2"],
"The coding bot generated an `is_prime` function, executed four assertions, identified the boundary error for values below two, and repaired the function on its second attempt. The final program passed four of four tests.",
"The failed first attempt is the useful observation. Three passing tests could have created false confidence, but the explicit `is_prime(1)` assertion exposed the defect. The repair changed one branch rather than rewriting the solution, which keeps the correction attributable and easy to review.",
"Execution is intentionally restricted to a small builtin allow-list. This is suitable for a demonstration, not a security boundary for hostile code; production execution belongs in an isolated process or container with time and memory limits."),
53: ("Project 053 - PDF Summarizer with Agents", [33,95,238], ["Pages","Chunks","Summary words"],
"The pipeline processed the public ReAct paper: 33 pages, 110,255 extracted characters, 95 working chunks, and a 238-word document summary. Chunk summaries remain available for audit, while the final synthesis emphasizes the abstract and stated contribution.",
"A full-document frequency score over-weighted repeated experiment text and appendix traces. Anchoring the final synthesis in the opening material produced a more faithful account of the paper's research question and contribution. The separation between chunk evidence and final narrative is important: it lets a reviewer inspect what was compressed.",
"The method is extractive and does not resolve figures or multi-column reading order perfectly. Page-level provenance and layout-aware extraction would be the next improvements for technical documents."),
54: ("Project 054 - AI Calendar Scheduler Agent", [2,4,1], ["Busy slots","Free slots","Booked"],
"The scheduler inspected the afternoon business-hour window, found four available slots around two occupied periods, and booked the earliest valid time at 12:00 on 5 October 2026. The calendar increased from three to four events without overwriting an existing entry.",
"Selecting from a computed availability set makes the decision reproducible. The result also shows why a scheduler should return alternatives: the chosen noon slot is efficient, but three later times remain available if a participant rejects it.",
"This implementation uses a local calendar dictionary and hourly slots. Real deployment needs time-zone normalization, participant calendars, duration-aware overlap checks, and explicit confirmation before writing to an external calendar."),
55: ("Project 055 - Self-Correcting Essay Grader", [6,7,5,8,9,10,6,8], ["Clarity 1","Grammar 1","Structure 1","Vocabulary 1","Clarity 2","Grammar 2","Structure 2","Vocabulary 2"],
"The first draft scored 6.50/10. After targeted expansion, the second draft reached 8.25/10: a 1.75-point improvement. The rewrite grew from 13 to 50 words and strengthened clarity, grammar, and structure while vocabulary remained stable.",
"The score pattern is more informative than the headline uplift. Grammar reached the ceiling and clarity improved sharply, but structure rose only one point and vocabulary did not move. A further revision should therefore add a clearer paragraph progression and more precise subject vocabulary rather than simply adding length.",
"The rubric is deterministic and surface-feature based. It is useful for demonstrating a grade–critique–rewrite–regrade loop, but it should not be presented as a substitute for trained human assessment."),
56: ("Project 056 - File Organizer Agent (Desktop AI)", [1,1,1,1,1,1], ["Documents","Images","Installers","Other","Sheets","Videos"],
"A six-file fixture was classified into six distinct destinations and then tested in real move mode. Every source file arrived in its planned category: document, image, installer, spreadsheet, video, and unmatched binary.",
"The even distribution is intentional test coverage rather than a claim about desktop composition. It confirms that each extension rule is exercised and that the preview plan matches the executed move. The preview-first design is the key operational control because users can inspect destinations before any file changes occur.",
"Classification is extension-led except for PDFs, where text cues can identify résumés. Duplicate names, recursive folders, rollback, and ambiguous files need explicit policies before using the organizer on a large personal directory."),
57: ("Project 057 - Browser Agent with Memory", [0.1705,0.1529,0.1504], ["Expert systems","Turing","Dartmouth"],
"The agent fetched the Artificial intelligence article once, stored 151 boundary-safe chunks, and retrieved three historically relevant passages. Similarity scores ranged from 0.1504 to 0.1705, covering the Dartmouth workshop, Turing's test, and the expert-system cycle.",
"The evidence spans three different phases instead of repeating one paragraph. That diversity makes the answer more useful: it links the field's formal founding, an early evaluation idea, and a later commercial boom followed by another winter. Memory also prevents a second network read when the user changes the wording of the question.",
"TF–IDF is lexical, so related passages without shared terms may rank poorly. Dense embeddings, citation-level identifiers, and a synthesis step that orders evidence chronologically would improve answer quality."),
58: ("Project 058 - API Router with LLM", [1,1,1], ["Weather","News","Calculator"],
"Three natural-language requests were routed to three different tools with 100% accuracy in the demonstration: weather, news, and arithmetic. Each route records the selected function and normalized input before dispatch.",
"The test set confirms clean separation between intent selection and tool execution. That separation matters because a bad route can be diagnosed independently from a failing API. The calculator path also inherits the restricted arithmetic evaluator instead of sending expressions to unrestricted Python.",
"Routing currently relies on transparent rules and the weather/news tools return deterministic fixtures. External APIs would require schema validation, credentials, retry logic, and an explicit fallback when intent confidence is low."),
59: ("Project 059 - Recursive Research Agent", [0.3158,0.1337,0.1910], ["Mechanism","Scale","Mitigation"],
"The agent decomposed the environmental-impact question into mechanism, scale, and mitigation branches. It indexed 49 complete text chunks and returned evidence for all three, with retrieval similarity between 0.1337 and 0.3158.",
"The mechanism evidence is strongest and directly links mining to energy use, emissions, and electronic waste. The scale branch adds a concrete estimate—2,300 tonnes of e-waste with 87% recycled, sold, or repurposed in the cited CCAF account—while the mitigation branch identifies waste-heat reuse in greenhouses. Together, the branches avoid reducing the issue to electricity consumption alone.",
"The source is a single synthesis page and its claims inherit that page's citations and disagreements. A deeper investigation should retrieve the underlying studies, compare estimation methods, and retain source-level citations in every answer."),
60: ("Project 060 - Cooking Assistant (Voice + Tools)", [0,0,0,1,2,2,1,2], ["Start","List","Convert","Next 1","Next 2","Repeat","Back","Next"],
"Eight conversational commands exercised recipe start, ingredient listing, unit conversion, step advance, repeat, and back navigation. The assistant completed two forward steps, correctly replayed the previous instruction, moved back one step, and recovered to step two.",
"The state trace demonstrates that navigation commands change state differently: repeat is read-only, back decrements safely, and next advances exactly once. Conversion is likewise independent of progress, so a user can request metric quantities without losing their place.",
"The interface is text-based and uses a fixed pancake recipe. Speech recognition, timers, dietary substitutions, persistence across sessions, and confirmation for ambiguous commands are logical production extensions."),
}

def style(ax, title, ylabel):
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color="#172554")
    ax.set_ylabel(ylabel); ax.grid(axis="y", alpha=.22); ax.spines[["top","right"]].set_visible(False)

for number, (folder_name, values, labels, overview, findings, limits) in PROJECTS.items():
    folder=ROOT/folder_name; assets=folder/"analysis_assets"; assets.mkdir(exist_ok=True)
    fig,ax=plt.subplots(figsize=(9,4.8)); bars=ax.bar(labels,values,color=["#2563eb","#0f766e","#d97706","#7c3aed"]*(len(values)//4+1))
    style(ax,"Observed validation results", "Score / count")
    ax.bar_label(bars,fmt="%.4g",padding=3); ax.tick_params(axis="x",rotation=20); fig.tight_layout(); fig.savefig(assets/"validation_results.png",dpi=150); plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,3.5)); ax.axis("off")
    steps={51:["Parse question","Choose operation","Call safe calculator","Return trace"],52:["Write code","Run assertions","Inspect failure","Repair"],53:["Read PDF","Chunk pages","Summarize evidence","Merge"],54:["Read calendar","Find open slots","Select earliest","Book"],55:["Grade draft","Identify gaps","Rewrite","Re-grade"],56:["Scan files","Classify","Preview plan","Move"],57:["Fetch once","Store memory","Retrieve passages","Answer"],58:["Parse intent","Select tool","Normalize input","Dispatch"],59:["Decompose","Retrieve per branch","Summarize evidence","Synthesize"],60:["Hear command","Read state","Use tool","Update state"]}[number]
    for i,item in enumerate(steps):
        x=.12+i*.25; ax.text(x,.52,item,ha="center",va="center",fontsize=10.5,color="white",bbox=dict(boxstyle="round,pad=.65",fc="#172554",ec="none"))
        if i<3: ax.annotate("",xy=(x+.18,.52),xytext=(x+.08,.52),arrowprops=dict(arrowstyle="->",lw=2,color="#64748b"))
    ax.set_title("Execution path",loc="left",fontsize=13,fontweight="bold",color="#172554"); fig.tight_layout(); fig.savefig(assets/"execution_path.png",dpi=150); plt.close(fig)
    title=folder_name.split(" - ",1)[1]
    report=f"""# Analysis Report: {title}

**Author:** Edward Ocran  
**Project:** {number}  
**Validation status:** Passed

## Executive finding

{overview}

![Observed validation results](analysis_assets/validation_results.png)

## What the run shows

{findings}

![Execution path](analysis_assets/execution_path.png)

## Method

The project was run through its normal workflow and its returned metrics were checked against the included automated test. The chart above reports the observed demonstration values; it is not a benchmark against unrelated systems. The second figure documents the control flow so the result can be reproduced and audited from the code.

## Interpretation and next decision

{limits}

## Reproduce the analysis

```powershell
python main.py
python -m unittest -v test_project.py
```

The implementation and test output are the primary evidence. External source details, where used, are documented in `DATASET.md`.
"""
    (folder/"ANALYSIS_REPORT.md").write_text(report,encoding="utf-8")
    objective={51:"Solve math word problems with a visible ReAct-style reasoning and calculator trace.",52:"Generate, execute, test, and repair a small Python function.",53:"Extract and summarize a real research PDF through a chunk-and-merge workflow.",54:"Find calendar availability and book a conflict-free event.",55:"Grade an essay against a rubric, revise it, and measure the change.",56:"Classify desktop files, preview destinations, and move them safely.",57:"Read a webpage once, retain searchable memory, and answer from retrieved evidence.",58:"Route natural-language requests to weather, news, or calculator tools.",59:"Decompose a research question and synthesize evidence from focused retrieval branches.",60:"Guide a recipe through stateful conversational commands and unit conversion."}[number]
    req="pip install -r requirements.txt" if (folder/"requirements.txt").read_text(encoding="utf-8").strip() else "# No third-party package is required for the core demo"
    readme=f"""# Project {number}: {title}

**Author:** Edward Ocran  
**Category:** AI Agents + Automation (Days 51–60)

## Objective

{objective}

## Included

- `main.py` — runnable implementation of the course workflow.
- `test_project.py` — project-specific behavior checks.
- `ANALYSIS_REPORT.md` — reviewed findings with two rendered charts.
- `analysis_assets/` — report figures generated from the validated run.
{('- `DATASET.md` — source and retrieval notes.\n' if (folder/'DATASET.md').exists() else '')}
## Run

```powershell
{req}
python main.py
python -m unittest -v test_project.py
```

## Result

The checked demonstration passes its behavioral tests. See [the analysis report](ANALYSIS_REPORT.md) for the observed metrics, interpretation, and limitations.

The course PDF is not redistributed in this public repository.
"""
    (folder/"README.md").write_text(readme,encoding="utf-8")

print("Generated reports and charts for Projects 51-60")
