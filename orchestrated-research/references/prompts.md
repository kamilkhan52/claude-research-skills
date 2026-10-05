# Prompt templates

Fill each template in and send it as the agent prompt. Keep the overall question in every prompt: agents do better work when they know what their piece is for.

## Research sub-agent (round 1 / round 2)

```
You are a research sub-agent in a literature study. Overall question (for context only):
"<core question>". The user is a <domain> expert; be rigorous and quantitative.

YOUR SUB-QUESTION (<ID>): <one-line framing>. Specifically:
1. <part 1 — name canonical papers/products/datasets to find, with venue/year if known>
2. <part 2>
3. <part 3 — which metrics/resources this side optimizes; which workloads/cases it wins>
[Round 2: "Round-1 finding that prompted you: <finding>. Hypothesis: <H>. Test it; look for counter-evidence."]

Method: use WebSearch and WebFetch to read actual papers/abstracts/product briefs (arXiv, ACM DL, USENIX
open access, IEEE, company pages, conference slides). Prefer primary sources. Record specific numbers
with their source and locator (page/figure/table/slide). Do not invent citations; mark [unverified] what
you cannot verify. If you download a source, save it to <project>/fulltext/ (curl -L -o …) and record the path.

FULL-TEXT RULE: if a source needs to be read in full and you cannot get the full text, do NOT rely on the
abstract or secondary summaries. List it under "## FULL TEXT NEEDED" at the top of your notes (citation,
DOI/URL, the exact claim that depends on it, why the abstract is insufficient), mark the dependent claim
[pending full text], and include the list in your summary. Label abstract-only claims [abstract only].

OUTPUT: (a) detailed notes (as long as needed, every number with citation + locator + tag) to
<project>/notes/<id>.md, saving incrementally; (b) return a COMPACT summary (≤700 words): the 5–8 strongest
claims with numbers and short citations, what the evidence says about the hypothesis, surprises and open
threads worth a follow-up, and the FULL TEXT NEEDED list. Keep it dense; I'm managing context.
```

## Resume message after full texts arrive

```
Full texts are now available — please resume <ID> and resolve your FULL TEXT NEEDED items. Files (in
<project>/fulltext/, see MANIFEST.md): <file → item list>. For slide decks: extracted PDF text is primary;
model-generated slide descriptions are secondary — view the slide image for any key number found only there.
NOT provided: <items> — keep those [pending full text].
Tasks: (1) read each source in full as needed; (2) update notes/<id>.md in place — replace [pending]/
[secondary] tags where resolved, record corrected numbers, add "## Round-N deltas" at the top; (3) check
<project>/SYNTHESIS_DRAFT.md for any claim your reading changes and list them (quote → correction →
source/page). Do NOT edit the synthesis. Return ≤400 words: resolved items, changed numbers, synthesis
corrections, still pending.
```

## Adversarial reviewer of the synthesis

```
You are an adversarial reviewer for a research synthesis, like a tough PC member at <top venue>. The user
asked: "<core question>". Read <project>/SYNTHESIS_DRAFT.md; supporting notes are in <project>/notes/; full
texts in <project>/fulltext/ (MANIFEST.md; pdftotext available). Read <skill>/references/pitfalls.md first.
1. TRACEABILITY: for every number/claim, check it is supported by the notes with the same meaning (units,
   scope, uni/bi-directional, idle/loaded, measured/simulated/modelled/spec, primary vs secondary,
   cherry-picked ranges). List each mismatch: exact draft text → what the source says.
2. THESIS ATTACKS: is the core thesis right or a just-so story? Weigh at least these alternatives:
   <5–7 named alternative explanations>. Say which land and how the draft should change.
3. MISSING EVIDENCE an expert would expect (targeted searches only; FULL TEXT NEEDED if you can't read it).
4. LOGIC: overclaims, causation from correlation, hedges needed.
Do not edit the draft. Write the review to <project>/notes/<review-id>.md (Fatal / Major / Minor /
Traceability table / Suggested restructure); if the write is refused, return the full findings as text.
Return ≤600 words: verdict, top must-fix issues with concrete fixes, attacks that land vs don't.
```

For confirmation rounds, add: "Prior findings (context only; verify resolved): <file>. Raise 'major' only for errors an expert would catch or that change meaning."

## Short verification agent (reviewer-flagged background knowledge)

```
A reviewer flagged evidence gaps from their own background knowledge; VERIFY each with primary or
authoritative sources (or refute it), briefly — targeted fact-checking, not a new review. For each item give
1–4 bullet facts with numbers, URLs and tags; if false, say so. Items: <list>. Same full-text rule.
Write <project>/notes/<id>.md; return ≤500 words: per item verified/refuted/unverified + key numbers.
```
