# File templates

## RESEARCH_LOG.md

```markdown
# Research log: <core question>
Started <date>.

## Ground rules
- (<user>, <date>) <rule, e.g. never rely on an abstract where a full text is needed; pause and ask>

## Full texts needed (waiting on user)
| Source | Needed for | Requested by | Status |
|--------|-----------|--------------|--------|

## Core question
<restated precisely; define operationally what the question's key terms mean (e.g., "both attractive", "why")>

## Working hypotheses (to be tested)
H1. …
H2. …

## Sub-questions -> agents (round 1)
| ID | Sub-question | Notes file | Agent id | Model | Status |
|----|--------------|-----------|----------|-------|--------|

## Round 2+ (launched <date>)
| ID | Sub-question | Notes file | Agent id | Model | Status |

## Findings so far
### Q1 (<topic>) — <date>
- <dense bullet with number + [tag] + source>

## Open branches / round-N candidates
- [R2 candidate] <branch> — why it could change the answer

## Decisions
- <date> vX: <what changed in the synthesis and why>
```

## FULLTEXT_REQUESTS.md

```markdown
# Full texts requested (drop PDFs into ./fulltext/ — any filename is fine)
## High priority (thesis-critical)
1. <Authors> — "<Title>", <Venue year>, doi:<…> — <claim it unlocks> [<agent>]
## Medium
## Low / optional
```

## fulltext/MANIFEST.md

```markdown
| Req# | Item | File | Assigned agent |
|---|---|---|---|
| — | <agent-downloaded item> | <file> | <agent> |
```

## ROUNDN_DELTAS.md

```markdown
# Round-N deltas to apply to SYNTHESIS vX -> vY
## <agent> (<sources read>) — received
1. <§> "<old text>" -> <correction> (<source, page/figure>)
```

## Canonical values (when a deck/report follows)

Keep `ORCH_NOTES.md`: one line per number that appears in more than one place, with its exact wording,
qualifier and source. It supersedes older notes; every downstream agent reads it.
