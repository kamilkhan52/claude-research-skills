# Instructions for figure-data agents (Phase 1)

You extract the data for ONE figure of a technical deck or report. Accuracy is the whole job.

Read:
1. <deck>/BRIEF.md: §B (global rules), §E (figure data specs: the row for YOUR figure, the common rules and the JSON envelope), and §D for the slide(s) that use your figure, including its "Evidence" and "do not say" lists.
2. The sources named in your §E row. Full texts are in <project>/fulltext/ (see MANIFEST.md; extract text with `pdftotext -layout`, and render pages with `pdftoppm -f N -l N -r 200 -png`, then view the PNGs with the Read tool when values are in figures or tables). Conference slide decks may be stored as extracted text plus slide images (see MANIFEST.md): extracted text is primary; any model-generated slide description is secondary, so view the slide image for any number found only there. Research notes are in <project>/notes/.

Rules:
- Use the JSON envelope from §E exactly. Every row carries src, loc (page/figure/table/slide), tag, unc and note.
- Use the row ids/keys the BRIEF specifies (e.g., `id`, `path`, `gen`) verbatim, so the two blind extractions can be compared mechanically.
- Prefer printed numbers over chart reads. For chart reads, state the axis type (linear or log) and your method (for example, pixel positions measured against labelled gridlines), and give a realistic uncertainty.
- Do not invent values. If a needed source is not readable in full, do NOT use its abstract. Write `"status": "FULL TEXT NEEDED: <item>"` for that row and continue with the rest.
- If you fetch an online source (WebFetch), save the PDF or HTML into <project>/fulltext/ (curl -L -o …) and record the path. Web search may be unavailable; use known URLs.
- Work independently. Do NOT open the other extractor's file (`<id>.json` vs `<id>.b.json`).
- Arithmetic you do is tagged D, with the formula in `unc`.

Output: write your JSON to the path given in your task. Return a compact summary (≤200 words): rows extracted, anything uncertain or missing, and any disagreement with the BRIEF's §D Evidence numbers (quote both).
