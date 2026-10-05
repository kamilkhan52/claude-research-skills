# Claude research skills

Two [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) for evidence-first technical research and for turning that research into presentations people can trust.

| Skill | What it does |
|---|---|
| [`orchestrated-research`](orchestrated-research/SKILL.md) | Runs a literature investigation as an orchestrator: breaks the question into sub-questions, gives each to a sub-agent that reads primary sources and writes notes to files, keeps a running research log, **pauses for full texts it cannot obtain instead of trusting abstracts**, follows surprising branches in later rounds, drafts a versioned synthesis, and hardens it with fresh adversarial reviewers until it survives. |
| [`evidence-deck-and-report`](evidence-deck-and-report/SKILL.md) | Turns a study into a white, technical HTML slide deck, an in-depth companion report, or a single illustrated explainer. Every number is provenance-tagged; charts are replotted from data two agents extracted independently; each slide is built by its own sub-agent from an architect's brief; accuracy, narrative and visual reviewers iterate until two clean rounds. Bundled `deck.css` and helper scripts (`assemble.py`, `check_layout.py`, `compare_extractions.py`, `verify_embeds.py`). |

They are designed to be used in sequence: research first, then the deck/report.

## Install

Copy either folder into your personal skills directory (or a project's `.claude/skills/`):

```bash
git clone https://github.com/kamilkhan52/claude-research-skills
cp -r claude-research-skills/orchestrated-research claude-research-skills/evidence-deck-and-report ~/.claude/skills/
```

Claude Code picks them up automatically; ask a "why does X happen" research question, or ask for a technical deck from a finished study.

The deck scripts need Python 3; rendering screenshots (`assemble.py --shots`) uses headless Google Chrome or Chromium if one is installed.

## Example output

[memory-proximity-paradox](https://github.com/kamilkhan52/memory-proximity-paradox) — the study these skills were distilled from: synthesis, research log, notes, 10-slide deck, companion report and explainer.

## Evals

Each skill has `evals/evals.json` with test prompts. The deck prompts refer to the example study at local paths; clone that repository and adjust the paths to run them. A first evaluation round favoured both skills over unassisted runs, but most runs were interrupted and resumed, so treat it as weak evidence.
