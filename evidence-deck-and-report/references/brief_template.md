# BRIEF.md: architect's brief (the single source of truth for every builder and extractor)

An Opus "deck architect" agent writes this from the reviewed synthesis, the plan, and the evidence. Builders follow it literally, so ambiguity here becomes inconsistency across slides. Sections:

## A. Thesis and narrative arc
- A.1 Thesis in ≤3 sentences.
- A.2 Arc table: # | section | what the slide establishes | hand-off to the next slide (e.g., "If not distance, then what?").

## B. Global rules for builders (copy, adapt)
1. **One claim per slide.** The `h2` headline is that claim: a full sentence of ≤16 words, copied exactly from §D. Count the words.
2. **Body text ≤ ~60 words per slide**, excluding figure labels, axis titles, captions, legends and tables. Count the words.
3. **Provenance tags live in the footer `.sources` line**, with page, figure, table or slide locators. Tags: [P] [P/V] [V] [Pr] [S] [D] [Syn] [unverified] [pend].
4. **Qualifiers go next to the number.** Flag vendor numbers inline (`V` chip or "vendor/projected"). Mark simulated "sim." and modelled "modelled". Peak specs say "peak"; measurements say "measured". Never present modelled or simulated as measured.
5. **Every value with a scope states it** (e.g., energy: I/O vs full access vs system; bandwidth: per direction vs total). Never compare across scopes. The only exception is a replot whose caption states the scope problem.
6. **Colour semantics are fixed** in deck.css: one meaning per colour across the whole deck. Neutral data uses ink greys with dash patterns.
7. **No dual axes.** Log scales are labelled "…, log scale" and use decade ticks.
8. **Every figure has a one-line caption** naming what is plotted and its source and uncertainty.
9. **Replot real data only.** Values come from `data/<id>.json`, embedded in the slide's `<script type="application/json" id="sNN-data">`. If a value is not in the JSON, it is not on the slide. Never paste screenshots.
10. **Labels and type.**
    - Direct labels beat legends.
    - SVG text is at least 11 px on a 1280 px slide. Use `.halo` on labels that cross lines.
    - Fonts only through CSS variables. Numbers use tabular figures.
    - Use "~", "–" for ranges, "×", µs, pJ/bit.
11. **Optional hover tooltips** via `window.DeckTip.attach(el, html)` carry full provenance. The slide must still read correctly without hover.
12. **Accessibility:** each SVG has `role="img"` and an `aria-label` sentence that is updated whenever the chart changes.
13. **Self-check before handing back:**
    - preview render: no overflow or clipping, nothing overlaps;
    - headline ≤2 lines; body ≤~60 words;
    - every number traceable to the data JSON or the Evidence list;
    - footer ≤3 lines, with ≥12 px clear above the footer rule.
14. **"Do not say" lists in §D are binding.**

## C. Fragment contract (copy exactly)
Each slide is `<deck>/slides/sNN.html` and contains:
- exactly one `<section class="slide" id="sNN" data-title="…">`, holding:
  - `<header class="slide-head">`: `div.kicker` "NN · Section", the `h2` headline, and an optional `div.sub`;
  - `<div class="slide-body">`;
  - `<footer class="slide-foot"><div class="sources">…</div><div class="pageno">NN / N</div></footer>`;
- optionally ONE `<script>` after the section, wrapped in an IIFE that only queries inside `#sNN`.

Other rules:
- Charts are inline SVG, static or built by JS from the slide's JSON data block.
- Slide-specific CSS goes in one `<style>` inside the section, with every selector starting `#sNN`. Do not edit deck.css.
- Element ids start with `sNN-`.
- Canvas is 1280×720 with 60 px side padding. The usable body area is about 1160×500 px when a `.sub` is present.

Preview: `python3 <skill>/scripts/assemble.py --root <deck> --preview sNN.html` writes `shots/sNN.png`.

## D. Per-slide specification (one block per slide)
- kicker · headline (exact) · sub (exact) · body copy (exact)
- layout (grid, sizes)
- figure spec (form, axes and scales, marks, encodings, annotations, data files and fields)
- footer (exact, with tags and locators)
- builder model (sonnet for chart-heavy slides, opus for argument-heavy ones)
- do-not-say list (known pitfalls)
- **Evidence** (not rendered): every number on the slide mapped to its notes or full-text location

## E. Figure data specs
- Common rules:
  - two blind extractions, with A writing `<id>.json` and B writing `<id>.b.json`;
  - the full-text rule;
  - copy fetched sources into `fulltext/`;
  - chart reads state the axis type and method, with uncertainty.
- JSON envelope:

  ```json
  {"id","version","slides":["sNN"],"title","units":{},"conventions":"…",
   "sources":{"key":{"cite","path","locator","tag"}},
   "rows":[{"<fields>","src","loc","tag","unc","note"}],
   "extraction":{"agent_a","agent_b","method","cross_check":{"max_disagreement","resolved"}},
   "caveats":[]}
  ```

- Table: # | data file | slides | fields (units) **and row keys** | source paths and locators | read from image? (axis type) | uncertainty field.
- Aim for ≤9 figures. Reuse already-reviewed data, such as an explainer's arrays, by copying it; the second agent then only spot-checks.

## F. Companion report outline
Sections mirror the slides. For each section, list the deeper points: mechanism, derivations with the arithmetic shown, caveats, counter-evidence, and "what the slide simplified". Appendices:
- method and provenance;
- full numbered reference list, with "where read" for each;
- pending full texts;
- what would change our mind;
- detailed derivations.

## G. Flags for the orchestrator
Table: issue | what the brief does | decision needed? Cover places where the brief departs from the synthesis or plan, new derived numbers, sources missing from `fulltext/`, and data that needs web fetches.
