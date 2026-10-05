# Instructions for deck reviewers (Phase 4 review loop)

You are a fresh reviewer of an N-slide technical deck. Audience and research question: see <deck>/BRIEF.md §A.

**Materials**

| What | Where |
|---|---|
| Slides (HTML fragments) | <deck>/slides/sNN.html |
| Assembled deck | <deck>/deck.html |
| Rendered screenshots (1280×720 slide on a 1340×760 canvas) | <deck>/shots/sNN.png (view with Read; regenerate all with `python3 <skill>/scripts/assemble.py --root <deck> --shots`) |
| Deck brief | <deck>/BRIEF.md: §A thesis/arc, §B rules, §D per-slide spec with Evidence and "do not say" lists |
| Figure data, reconciled from two blind extractions | <deck>/data/*.json (see each file's extraction.cross_check and caveats; ignore *.b.json) |
| Known cross-slide items the orchestrator already logged | <deck>/reviews/ORCH_NOTES.md (verify they are fixed; don't just repeat them) |
| Reviewed answer the deck must reflect | <project>/SYNTHESIS_vX.md (current version) |
| Evidence base | <project>/notes/*.md; full texts in <project>/fulltext/ (MANIFEST.md; `pdftotext -layout`, `pdftoppm -r 200 -png` for pages) ; slide-deck sources as extracted text plus images (see MANIFEST.md) |
| Pitfall catalogue and earlier reviews | <research-skill>/references/pitfalls.md; <deck>/reviews/r*_*.md |

**Rules**
- Be specific and actionable. Every finding gives: slide id; severity (blocking / major / minor); the exact element or text; what is wrong; the correct value or wording with its source and locator; and a concrete fix.
- Blocking: a factual error, a misleading chart, or a claim the evidence does not support.
- Major: a scope mismatch, a missing or wrong qualifier (measured / simulated / modelled / vendor / projected), a cross-slide inconsistency, a chart-integrity problem, an illegible or overlapping element, or a narrative gap.
- Minor: polish.
- Never rely on an abstract where a full text is needed. Flag "FULL TEXT NEEDED" instead.
- Do not edit slides. Write your review file and return a summary. If your write is refused, return the full findings as text.
- In confirmation rounds, raise "major" only for errors an expert would catch or that change meaning, or for defects visible at presentation size.

**Output**
- Write your review to the path given in your task.
- Return ≤300 words: verdict ("ready" / "needs revision"), counts by severity, and the blocking and major items in one line each.
