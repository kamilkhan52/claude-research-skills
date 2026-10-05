# Companion report and single-question explainer

## Companion report (Opus writer, started in parallel with deck review round 1)

Prompt essentials:
- **Inputs:**
  - BRIEF §A, §D (Evidence, do-not-say) and §F
  - the synthesis
  - the slide fragments and screenshots
  - data JSON (authoritative), ORCH_NOTES and all decisions files
  - notes, full texts, pitfall catalogue
- **Output:** a single self-contained HTML page (`deck/report.html`). Set the `<title>` first and link Google Fonts. The design tokens are copied from deck.css, white, single light theme. It has a ~70ch reading column with full-width figures.
- **Structure:**
  - **Title and front matter:** title, an abstract of ≤150 words, and a "how to read" note (tag legend and energy-scope labels), with a table of contents and figure list right under the title.
  - **Sections 1–N:** one per slide, mirroring it. Each opens with the slide's headline claim. Then come the mechanism, derivations with the arithmetic shown, caveats, counter-evidence and "what the slide simplifies".
  - **Appendices:** method and provenance (including the two-blind-extraction method and the review rounds), a numbered reference list with where each source was read (fulltext path / supplied / online / via notes), pending full texts, what would change our mind, and detailed derivations.
- **Figures:** re-implement the slide figures at report width. They are inline SVG built from **verbatim** copies of the data JSON, embedded as `<script type="application/json" id="data-<id>">`. Add a few figures and tables that appear only in the report where they help.
- **Rules:**
  - Inline provenance tags after numbers are allowed in the report, unlike the slides.
  - Every number must be traceable.
  - No paragraph over ~120 words.
  - Define jargon at first use and add a glossary.
  - Tags must be ≥11 px with real contrast.
  - Wide figures go in overflow-x containers with a min-width and a visible scroll cue.
  - Plain technical English, with no em-dash asides and no "not X but Y".
- **Length:** about 7–9k words of body.
- **Save incrementally.** The page is about 45k px tall, so render-check with per-figure element screenshots (Playwright) or with tall windows and crops.
- **After any data-file change:** re-embed the data and run `scripts/verify_embeds.py report.html data/`.

Publish with a status banner if the user wants it before the loop converges, then remove the banner on the final publish.

## Single-question explainer (one illustrated page answering a clarifying question)

Use this when the user asks "explain X" about a claim inside the research and wants a visual. It is the same craft at a smaller scale.

1. **Answer from first principles.** Write it out as equations, for example:
   - BW = wires × rate
   - P = BW × E
2. **Build the page.** Use 2–3 figures:
   - a schematic, labelled "not to scale";
   - a to-scale geometry drawn from vendor dimensions;
   - a replotted vendor or paper chart with derived overlays such as constant-power lines.

   Give every number a tag. End with a "what the sentence gets right / where it is loose" section and a general-principle box.
3. **Run three accuracy rounds with fresh Opus reviewers.**
   - The reviewers get the slide images and full texts, not just text.
   - Expect round 1 to find blocking errors: vendor footnotes, the wrong mechanism, scope mixing.
   - Expect round 2 to find major attribution and scope errors, including errors the round-1 reviewer introduced.
   - Round 3 confirms.
4. **Publish as an Artifact, then fold the corrected framing back into the synthesis** as a new version.
