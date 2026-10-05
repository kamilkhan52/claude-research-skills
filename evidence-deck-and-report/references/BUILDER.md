# Instructions for slide builders (Phase 2)

You build ONE slide of an N-slide technical deck. The audience is given in BRIEF.md §A. Craft and accuracy matter more than speed.

Read:
1. <deck>/BRIEF.md: §A (thesis and arc, so you know where your slide sits), §B (global rules; binding), §C (fragment contract; binding), and §D for YOUR slide: exact headline, sub, body copy, layout, figure spec, footer, "do not say" list and Evidence.
2. <deck>/assets/deck.css: the available classes and colour semantics. Do not edit it.
3. Your data file(s) in <deck>/data/ if your slide uses any. Use only `<id>.json` (the reconciled file), never `.b.json`. Copy the values you plot into the slide's `<script type="application/json" id="sNN-data">` block. Nothing is plotted that is not in the data.
4. If you need the original source to understand a number, the full texts are in <project>/fulltext/ and the notes in <project>/notes/.

Build <deck>/slides/sNN.html to the fragment contract.

**Design.**
- White background, quiet and precise.
- Fixed colour semantics as defined in deck.css and BRIEF.md §B (each semantic colour means one thing across the whole deck).
- Direct labels; recessive gridlines; thin marks.
- Charts are drawn to scale, and every tick and label names a value on the scale.
- Minimum SVG text is 11 px. No dual axes. Log scales are labelled.
- One idea per slide; whitespace is part of the design.
- If the BRIEF's layout does not fit the canvas, adapt the layout. Never change the text content or numbers. Report any adaptation.

**Verify before you finish.**
- Run `python3 <skill>/scripts/assemble.py --root <deck> --preview sNN.html` and view `<deck>/shots/sNN.png` with Read.
- Fix overflow, clipping, overlaps, illegible labels and misaligned elements. Iterate until clean, at most 4 renders.
- Then self-check the BRIEF §B rule 13 (self-check).

Return a compact summary (≤150 words): what you built, layout adaptations, any number you could not trace, and anything you think the BRIEF got wrong.
