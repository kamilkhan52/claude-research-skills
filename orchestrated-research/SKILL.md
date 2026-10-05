---
name: orchestrated-research
description: "Run a deep, evidence-first literature investigation of an open research question as an orchestrator that decomposes the question into sub-questions, delegates each to a sub-agent that reads primary sources and writes notes to files, keeps a running research log, pauses for full texts it cannot obtain instead of trusting abstracts, follows surprising branches in later rounds, drafts a synthesis, and hardens it with fresh adversarial reviewers until it survives. Use whenever the user asks a 'why'/'how come'/'what explains' question about a technical field, wants a systematic literature review, says 'think like a researcher', 'read the papers', 'break this into sub-questions', 'use sub-agents', or wants an evidence-backed answer to a question that spans many papers, products or data sources — even if they don't say 'literature review'. Not for quick factual lookups or single-paper summaries."
---

# Orchestrated research

A procedure for answering a hard research question with a team of sub-agents while keeping your own context small and every claim traceable. It was distilled from a multi-day study ("why are memory–compute coupling and memory disaggregation both attractive?") that went through five research rounds, four full-text rounds supplied by the human, and more than a dozen adversarial reviews. The rules here each prevent a failure that actually happened.

**Roles.**
- **The human** owns the question, supplies full texts, and makes judgment calls.
- **The orchestrator** (you):
  - decomposes the question, writes prompts and keeps the log;
  - triages agent results, decides the next branches and writes the synthesis;
  - does **not** read papers in bulk itself, so that its context stays free for judgment.
- **Research sub-agents** each own one sub-question. They read primary sources, write detailed notes to a file and return only a compact summary.
- **Fresh reviewer agents** see the synthesis and the notes cold and try to break both.

A single agent never reviews its own work.

## 0. Confirm the question

Before fanning out:
1. Restate the question in about five lines, with your first hypotheses and the audience.
2. Ask the user for standing rules: full-text policy, path conventions, depth and budget, the deliverable.
3. If they don't answer, proceed on defaults. The defaults are this skill's rules, `~/research/<slug>/`, and a synthesis in Markdown.

**Prerequisites:** WebSearch and WebFetch (search quota can run out, so fall back to fetching known URLs, such as arXiv PDFs), `pdftotext` and `pdftoppm` from poppler, and `python3`.

**Agent mechanics:**
- Spawn agents with the Agent tool: `run_in_background: true`, and `model: "opus"` for judgment or `"sonnet"` for extraction.
- Record each agent id in the log's sub-question table.
- Resume an agent with SendMessage to its id; it keeps its context.
- Launch independent agents in one message so they run in parallel.

## 1. Set up the record first

1. **Project directory.** Create `~/research/<slug>/` (no spaces) with:
   - `RESEARCH_LOG.md`, from the template in `references/templates.md`
   - `notes/`, one file per sub-question or round
   - `fulltext/`, every source actually read, plus `MANIFEST.md`
   - `archive/`, superseded synthesis versions
2. **The log.** Keep it current after every agent result, as the single entry point for resuming after compaction or a restart. It holds:
   - the core question
   - working hypotheses (H1…Hn)
   - a sub-question table (ID, question, notes file, status)
   - findings per sub-question, in a few dense bullets with numbers and tags
   - open branches and round-N candidates
   - a "Full texts needed" table
   - decisions with dates
3. **Ground rules in the log.** Write the user's standing rules into the log the moment they state them, and copy them into every later agent prompt. Examples: "never rely on an abstract where a full text is needed", "no spaces in paths".

## 2. Decompose, then fan out (round 1)

- **Hypotheses before agents.** Write 3–5 falsifiable hypotheses first. They tell you which sub-questions matter and give the synthesis something to confirm or refute.
- **Round-1 sub-questions.** Choose four to six that together cover the question. A pattern that worked for "why are X and Y both attractive?":

  | # | Sub-question |
  |---|---|
  | Q1 | The case for X, with quantitative evidence and products |
  | Q2 | The case for Y, the same way |
  | Q3 | Shared root causes and trends: technology, economics, scaling laws. Ask for a consolidated comparison table. |
  | Q4 | Which properties of the workload, data or users make each option pay off. Ask for the unifying framework, if one exists. |
  | Q5 | The strongest critiques and failures of each, and where the two converge |

- **Launch them together** in one message as background agents. Use the prompt template in `references/prompts.md`. Every prompt says:
  - the overall question, for context;
  - the agent's sub-question, in numbered parts naming the canonical papers and products the agent should find;
  - "prefer primary sources, record numbers with sources, mark [unverified] what you cannot verify";
  - the full-text rule (§4);
  - output: detailed notes to `notes/<id>.md`, plus a compact summary of at most ~700 words returned to you.
- **Reading agent output.** You see only the returned summary, never the transcript. Fold each summary into the log's Findings and its Full-texts-needed table as it arrives. Then tell the user, in plain language, what came back and why it matters.

## 3. Follow the surprises (round 2+)

Round-1 summaries surface things nobody planned for: a mechanism that couples the two answers, a historical precedent, a derived quantity that unifies everything.

- Write each as an `[R2 candidate]` in the log with one line on why it could change the answer.
- Launch the strongest two or three as new agents.
- Do small derivations yourself with a script, tagged [D]. A unifying table built from numbers already in the notes is an example.

Good round-2 targets from experience:
- the economic or supply-side coupling between the options;
- the historical precedent: did the same split happen before, what killed or saved each side, and what is different now;
- a rigorous derivation of the quantity your thesis rests on.

## 4. The full-text rule

When a source must be read in full and the agent cannot get it (paywall, a blocked PDF, a slide deck that returns 401), the agent must not fill the gap from the abstract, a press summary or its own memory. Instead it:

1. writes the item under `## FULL TEXT NEEDED` at the top of its notes: citation, DOI or URL, the exact claim that depends on it, and why the abstract is insufficient;
2. marks the dependent claim `[pending full text]`, and labels anything taken from abstracts `[abstract only]`;
3. lists the item in its returned summary.

The orchestrator then:
- merges every request into `FULLTEXT_REQUESTS.md`, prioritised (thesis-critical first);
- asks the user once, in a batch, for the PDFs, suggesting they drop files into `fulltext/` with any name.

When files arrive:
1. Identify each with `pdftotext -l 1`.
2. Map files to requests and to the agents that asked, in `fulltext/MANIFEST.md`.
3. For slide archives, extract the relevant decks to text, and keep the images available for checking numbers.
4. Resume the original agents by ID with SendMessage. Each updates its notes in place under a "Round-N deltas" heading, and lists every claim in the synthesis that its new reading changes, quoting the old text, giving the correction and naming the source. Agents never edit the synthesis themselves.
5. Collect those corrections in `ROUNDN_DELTAS.md`, then apply them yourself as the next synthesis version.

When an agent downloads a source itself, copy it into `fulltext/` the same turn. Session scratchpads disappear, and later reviewers need the file.

## 5. Synthesis, versioned

- **Writing it.**
  - Write `SYNTHESIS_DRAFT.md` and archive every version (`archive/SYNTHESIS_vX.md`).
  - Lead with a short answer, then sections for the mechanism, the evidence and the counter-evidence.
  - Weigh the alternative explanations, give implications, and add a "what would change our mind" section.
- **Tags.** Every number carries a provenance tag. Legend:

  | Tag | Meaning |
  |---|---|
  | [P] | Primary, read in full |
  | [P/V] | Primary, but from an interested seller |
  | [V] | Vendor |
  | [Pr] | Press |
  | [S] | Secondary |
  | [D] | Our arithmetic |
  | [Syn] | Our synthesis |
  | [pend] | Pending a full text |
  | [unverified] | Not verified |

- **Scope and qualifiers.**
  - State the scope of any figure that has one, for example energy as "I/O vs full access vs system".
  - Say whether each result is measured, simulated, modelled, emulated, a spec or a projection.
- **Prefer a decision-useful framing to a list.** For example, in a memory-systems study the answer became a two-axis cost frontier plus a deployed-vs-ambitious 2×2. That framing came from a reviewer attacking the first draft's single-axis thesis. Expect the framing to move.

## 6. Adversarial review until it survives

Spawn a fresh reviewer (Opus) with the draft path, the notes directory and the full-text directory. Its prompt is in `references/prompts.md`. It must return:

- **Traceability:** every number in the draft checked against the notes, with mismatches listed: unit, scope, uni- vs bi-directional, idle vs loaded, secondary presented as primary, cherry-picked ranges.
- **Thesis attacks:** at least five named alternative explanations and their verdicts. Typical ones:
  - it is really different markets;
  - vendor incentives and hype;
  - different research communities;
  - the metric you ignored matters more;
  - the table mixes incomparable numbers;
  - the "opposite" framing is a misreading.
- **Missing evidence** an expert would expect.
- **Logic:** correlation presented as causation, overclaims, a single-axis story that cannot explain the data.
- A **suggested restructure**.

Then:
- **Triage.** Accept, reject with a reason, or defer each finding, and log the decisions. Rewrite the synthesis, reusing the reviewer's fixes where they are right.
- **Source new evidence.** When a reviewer names evidence from background knowledge, launch a short verification agent before using it.
- **Next round.** Run another fresh reviewer on the new version.
- **Stop rule:** stop when two consecutive fresh reviews find nothing blocking or major. Three rounds was typical for a single page; the full synthesis took two reviews plus a full-text round.

**Corrections from the human.** When the user asks a clarifying question, answer it from first principles, separating what limits what. Fold the corrected framing back into the synthesis as a new version. The user's question often reveals a compressed sentence that was wrong.

## 7. Model allocation, quota and resilience

- **Opus:** judgment work. Decomposition prompts, research agents on contested topics, adversarial reviews, synthesis rewrites.
- **Sonnet:** mechanical but careful work. Data extraction from figures and tables, citation and traceability audits, fix application against a checklist, visual QA.
- **Never race two models on the same task.** Use one primary and a sequential fallback.
- **Agents save incrementally.** Tell long-running agents to write their file after each section, because an API limit or a restart kills an agent mid-task and anything unsaved is lost. After an interruption, inspect the files on disk (timestamps, grep for expected fixes) before relaunching, and resume from what exists.
- **Refused writes.** If a reviewer's write is refused, it must return its findings as text. Save them to the review file yourself before acting on them.
- **Publish early on request.** If the user asks for the content while loops are still running, publish the current state with a clear status banner ("draft under revision; known open items: …"), then continue.

## 8. Pitfall catalogue

Read `references/pitfalls.md` before writing any synthesis, and give it to every reviewer. It lists errors that reviewers caught in practice, each with a check. Examples:
- vendor footnotes that redefine a number ("GPU power 1,200 W" is not package power);
- energy figures with different scopes compared directly;
- a spec estimate quoted as a measurement;
- an emulation called "pre-production hardware";
- trace replay called "production";
- a ratio whose denominator the paper never defines;
- a circular citation chain ("50% of server cost");
- the orchestrator's own prescribed wording introducing a new error.

## 9. Hand-off

The handoff to the deck skill consists of:
- `SYNTHESIS_vX.md`, the reviewed answer;
- `notes/`;
- `fulltext/` with `MANIFEST.md`;
- the log;
- a canonical-values file (`ORCH_NOTES.md`) if you started one.


When the answer is final:
- Give the user the short answer in chat, with the main evidence and the main caveats.
- Point to `SYNTHESIS_vX.md`, the log and the outstanding full-text list.
- Offer to turn the result into a deck, report or explainer with the `evidence-deck-and-report` skill.
- Save a project memory pointing to the directory, the deliverables and the open items.
