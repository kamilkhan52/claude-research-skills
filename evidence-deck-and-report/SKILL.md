---
name: evidence-deck-and-report
description: "Produce a meticulous, evidence-backed technical presentation (HTML slide deck), a companion in-depth report, or a single illustrated explainer page, in a clean white technical style. Every number is provenance-tagged, charts are replotted from paper and slide data that two agents extracted independently, each slide is built by its own sub-agent from an architect's brief, and fresh accuracy, narrative and visual reviewers iterate until two clean rounds. Use when the user wants research findings or a literature study turned into a technical slide deck, talk, in-depth report or write-up, or wants a claim explained with an accurate illustration — especially when they ask for accuracy reviews, replotted figures from papers, sub-agents per slide, or review loops, or right after an orchestrated-research study. Not for quick one-off charts, marketing/sales decks, ordinary documents without a research evidence base (use the docs skill), or requests for .pptx/PowerPoint files (use the pptx skill)."
---

# Evidence deck and report

A production pipeline for a technical deck plus a companion report (or a one-page explainer) that a domain expert can trust number by number. It was distilled from a 10-slide deck and a ~9k-word report on memory–compute coupling vs disaggregation. That work took two blind extractions per figure and seven deck review rounds. Each rule below exists because skipping it produced an error a reviewer caught.

Pair it with the `orchestrated-research` skill. That skill produces the synthesis, notes, `fulltext/` and pitfall catalogue that this one consumes. When those don't exist, run at least a light version of it first: slides cannot be more accurate than the evidence behind them.

## Before you start

**Placeholders** used throughout this skill and its reference files:

| Placeholder | Meaning |
|---|---|
| `<skill>` | `~/.claude/skills/evidence-deck-and-report` |
| `<research-skill>` | `~/.claude/skills/orchestrated-research` |
| `<project>` | `~/research/<slug>`, the research project directory |
| `<deck>` | `<project>/deck` |

**Input.** The handoff from research is:
- `<project>/SYNTHESIS_vX.md`, the reviewed answer;
- `<project>/notes/` and `<project>/fulltext/` (with `MANIFEST.md`);
- the research log.

**Prerequisites:**
- Chrome or Chromium; set `CHROME=/path` if it is not in the default location.
- `python3` with Pillow and numpy.
- poppler (`pdftotext`, `pdftoppm`).
- Optional: Playwright, for element screenshots of long reports.

**Setup:**
```bash
mkdir -p <deck>/{assets,slides,data,build,shots,reviews}
cp <skill>/assets/deck.css <deck>/assets/
python3 <skill>/scripts/assemble.py --help   # all four scripts print their usage with --help
```

**Agent mechanics.** Spawn agents with the Agent tool (`run_in_background: true`, `model: "opus"` or `"sonnet"`). Record each agent id in a registry (`<deck>/build/agents.json`: role → id), and resume an agent with SendMessage to its id. Resumed agents keep their context, which makes fix rounds cheap and consistent.

**Artifacts.** Before the first publish, follow the Artifact tool's own rules. Run its quickstart call if the session requires one, and load `artifact-design`. Then reconcile them with this skill's deliberate choices:
- the single white light theme, which is a stated exception to dark-mode support;
- fixed 1280×720 slides, scaled down on narrow screens by the assembler.

## Style (what the output looks like)

- **Visual design**
  - White background, single light theme by choice.
  - IBM Plex Sans body text, Source Serif 4 headlines, IBM Plex Mono for data and tags.
  - Quiet greys, with four semantic accent colours. Each colour has one meaning across the whole deck, such as option A, option B, the baseline, and convergence.
- **Slides**
  - Fixed 1280×720 slides with keyboard navigation and a present mode (P, arrows, Home/End, Esc, swipe).
- **Each slide carries:**
  - a kicker;
  - one-claim headline, a full sentence of at most 16 words;
  - an optional subtitle;
  - a body of about 60 words or fewer, plus figures;
  - a footer line of sources with provenance tags and page, figure or slide locators.
- **Figures**
  - Inline SVG, drawn to scale, with direct labels, recessive gridlines and labelled log axes, and no dual axes.
  - A one-line caption giving the source and its uncertainty.
  - Hover tooltips with full provenance.
- **Qualifiers sit next to the number:** measured, simulated, modelled, spec, vendor, projected, typical, and the scope of any energy figure. The tag legend is `[P] [P/V] [V] [Pr] [S] [D] [Syn] [pend] [unverified]`.
- **Where things live:** `assets/deck.css` holds the design tokens, and `scripts/assemble.py` holds the deck chrome and navigation. Before inventing a new look, load the `artifact-design` and `dataviz` skills only where they add something, such as palette validation.

## Pipeline

Lay out a project directory `<project>/deck/` containing:
- `BRIEF.md` and `PLAN.md`
- `assets/deck.css`, copied from this skill
- `slides/`, `data/`, `build/`, `shots/`, `reviews/`

Keep a progress line in the project's research log after every phase.

### 0. Plan, then confirm with the user
Write `PLAN.md`:
- the storyline, one claim per slide;
- the main figure per slide;
- the phases and the model allocation;
- the stopping rule;
- open choices with defaults (format, publishing, data that is only secondary).

Show it and get a go-ahead before spending agents.

### 1. Architect's brief (Opus, one agent)
The brief is the single source of truth. Follow `references/brief_template.md`:
- A: thesis and arc
- B: global rules
- C: fragment contract
- D: per-slide specs with exact copy, Evidence lists and do-not-say lists
- E: figure data specs with row keys
- F: report outline
- G: flags

Resolve the brief's flags with explicit decisions, and copy any session-scoped downloads into `fulltext/` before extraction starts.

### 2. Figure data: two blind extractions per figure (Sonnet)
- **Launch:** for each data file in brief §E, launch extractor A (writes `data/<id>.json`) and extractor B (writes `data/<id>.b.json`) in parallel, with `references/FIGURE_AGENT.md`. Copy data that was already reviewed (for example, from an explainer) instead of re-extracting it, and have one agent spot-check it.
- **Reconcile:** run `scripts/compare_extractions.py`. Go back to the source on any disagreement beyond tolerance, and record the outcome in `extraction.cross_check`. Extractions often disagree on *interpretation* (definitional values, ranges vs points, denominators) more than on numbers, so read both agents' caveats.
- **Start building early:** start builders for slides that need no data at once, and build each other slide as soon as its data is reconciled.

### 3. Slides: one builder agent per slide
- **Model:** Sonnet for chart-heavy slides; Opus for argument-heavy ones (opening, 2×2-style synthesis, implications).
- **Instructions:** use `references/BUILDER.md`. Builders preview with `python3 <skill>/scripts/assemble.py --root <deck> --preview sNN.html`, inspect the PNG, and iterate (at most 4 renders).
- **Keep a builder registry** (slide → agent id) so you can resume the *same* builder for fixes; it keeps its context.
- **After all slides exist:**
  - run `assemble.py --root <deck> --shots`, then `scripts/check_layout.py --root <deck>`, which checks footer-rule position and clearance and writes a contact sheet;
  - look at the contact sheet yourself before the first review.

### 4. Deck review loop
Follow `references/review_loop.md`:
- **Each round:** three fresh reviewers (accuracy Opus, narrative Opus, visual Sonnet) using `references/REVIEWER.md`.
- **Triage:** you write a binding `reviews/rN_decisions.md` and update the canonical `reviews/ORCH_NOTES.md`.
- **Fixes:** dispatch them to the original builders. Apply trivial fixes yourself. Then rebuild and run the layout check.
- **Stop:** when a dimension has two consecutive rounds with no blocking or major findings. This is the same stopping rule the research skill uses for its synthesis, applied separately to accuracy, narrative and visuals.

Your own decision wording gets reviewed too: one orchestrator-prescribed phrase was wrong for two of three cited systems.

### 5. Companion report (Opus writer; can start in parallel with deck round 1)
See `references/report_and_explainer.md`. Embed verbatim copies of the data and run `python3 <skill>/scripts/verify_embeds.py <deck>/report.html <deck>/data` after every data change.

The report review loop has three reviewers: Opus technical, Sonnet citations and traceability, Sonnet visual. Corrections the report reviewers find often apply to the deck and the synthesis too, so propagate them.

### 6. Publish
Publish each artifact (Artifact tool, private by default) and keep the same file path so updates keep the URL:
- `deck.html`, copied to a descriptive filename;
- `report.html`;
- the explainer.

If the user asks to see work before convergence, publish with a status banner listing the known open items, then republish without it. Tell the user who can open the links (private until shared). Save a project memory with the URLs, paths and open items.

## Single-question explainer
When the user asks to "explain this sentence/claim with an accurate illustration", build one page instead of a deck:
1. a first-principles answer;
2. 2–3 figures (a schematic, a to-scale geometry, a replotted chart with derived overlays);
3. "right / loose" verdict sections;
4. **three** fresh Opus accuracy rounds with access to slide images and full texts.

Details are in `references/report_and_explainer.md`. Fold the corrected framing back into the synthesis.

## Resilience
- **Quota and restarts:** agents hit quota limits and computers restart. Tell long-running writers to save incrementally.
- **After an interruption:** audit the disk state before relaunching. Check timestamps, grep for expected fixes, and run `verify_embeds.py` and `check_layout.py`.
- **When the Opus quota runs out:** use the Sonnet checklist fallback in `references/review_loop.md`, and tell the user plainly which checks were not done by Opus.
- **Refused writes:** if a reviewer's write is refused, it returns its findings as text; save them yourself.
- **Communication:** keep the user informed in plain language after each agent result: what came back, what changed, what is still running.

## Bundled files
| Path | Use |
|---|---|
| `assets/deck.css` | Design tokens, slide frame, building blocks, SVG classes, deck chrome |
| `scripts/assemble.py` | Assemble fragments → deck.html; `--shots` renders every slide; `--preview` renders one (`--root`, `--title`) |
| `scripts/check_layout.py` | Footer-rule y and clearance per slide, flags wrapped footers, writes the contact sheet |
| `scripts/compare_extractions.py` | Diff two blind extractions by row key and numeric fields |
| `scripts/verify_embeds.py` | Check that embedded JSON in an HTML page equals the current data files |
| `references/brief_template.md` | BRIEF.md structure, global rules, fragment contract, data envelope |
| `references/FIGURE_AGENT.md`, `BUILDER.md`, `REVIEWER.md` | Instructions each agent reads (replace `<deck>`, `<project>`, `<skill>`) |
| `references/review_loop.md` | Reviewer line-up, triage, decisions/ORCH_NOTES, stopping rule, quota fallback |
| `references/report_and_explainer.md` | Report writer brief and the explainer workflow |
