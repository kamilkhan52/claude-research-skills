# Review loops, decisions files and canonical values

## Reviewer line-up per round (fresh agents every round; never reuse a reviewer)

| Artifact | Reviewer | Model | Focus |
|---|---|---|---|
| Deck | Technical accuracy and traceability | Opus | Every number, qualifier, energy scope, tag and claim, checked against data JSON, notes, full texts and slide images; cross-slide consistency; whether ORCH_NOTES items are fixed |
| Deck | Narrative and editorial | Opus | Does the deck answer the question? One supported claim per headline (≤16 words, counted); arc and hand-offs; density (word counts); terminology; faithfulness to the synthesis; rival explanations acknowledged |
| Deck | Visual QA | Sonnet | Screenshots and PIL crops: overlaps, clipping, text <11 px, contrast, footer clearance, alignment, colour semantics, chart integrity, density and hierarchy |
| Report | Technical | Opus | As for the deck, plus the derivations, re-checking the arithmetic |
| Report | Citations and traceability | Sonnet | Script-extract every number and tag, then spot-check ≥40 against full texts. Reference list: no orphans, paths exist, tags honest. Same quantity, same value everywhere. Embedded data equals the data files |
| Report | Visual and readability | Sonnet | Per-figure crops at 1100 and 500 px; TOC and figure list; heading hierarchy; paragraph length; glossary; narrow-screen figures |

Every reviewer prompt includes the materials table from `REVIEWER.md`, the pitfall catalogue, the previous round's findings ("verify resolved"), and the decisions files.

## Orchestrator triage after each round
1. **Save findings first.** If a reviewer's file write was refused, save its returned findings to `reviews/<artifact>_rN_<role>.md` yourself before acting on them.
2. **Write `reviews/rN_decisions.md`.** It is binding and supersedes earlier decisions and the BRIEF. Structure:
   - **Global items:** canonical value changes, terminology, spacing.
   - **Per-slide items:** exact replacement text, which keeps builders from improvising.
   - **Approved headline rewrites:** each word-counted, at most 16 words.
   - **Declined findings,** with the reason.
3. **Update `reviews/ORCH_NOTES.md`.** It is the canonical-values file: one line per number or wording used in more than one place (value, qualifier, source). Supersede older lines explicitly.
4. **Propagate every canonical change everywhere**, the same turn: the data JSON, the synthesis (new version), the report's embedded data, and the explainer. Stale copies were the most common recurring defect.
5. **Dispatch fixes.** Send each slide's fixes to its *original* builder via SendMessage, which resumes the agent with its context. Make the messages short: point to the decisions file and the review entries for that slide, and ask for a return of ≤80 words.
6. **Apply trivial fixes yourself.** Do one-line label or sign fixes and footer trims directly with exact-string edits. Then re-render and run `scripts/check_layout.py`. A footer that wraps to a fourth line moves the rule, and the script flags it.
7. **Rebuild, re-render and check layout**, then launch the next round.

## Stopping rule
- **Per dimension:** a dimension is done after two consecutive fresh rounds with no blocking and no major findings. Track accuracy, narrative and visual separately; a dimension that is done drops out of later rounds.
- **Re-check your own edits:** if the orchestrator's own edits after the last clean round changed numbers, run one more accuracy confirmation.
- **When stopping:** list the remaining minors and open items (missing full texts, unverifiable numbers) in the delivery message.
- **Typical cost:** the 10-slide deck took 7 rounds to converge. Rounds 1–2 found real errors, and rounds 5–7 found mostly one-line consistency issues.

## Model-limit fallback
If the Opus quota runs out mid-loop:
1. Audit the on-disk state with scripts (grep for expected fixes; `verify_embeds.py`).
2. Finish the fixes with a Sonnet agent that works from an explicit checklist and writes a fix log (DONE before / FIXED now / NOT FIXED + reason).
3. Run a Sonnet confirmation review.
4. Tell the user which review was done by Sonnet instead of Opus, and offer an Opus re-check after the reset.
