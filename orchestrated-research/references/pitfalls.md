# Pitfall catalogue: errors reviewers caught in practice

Give this file to every synthesis writer and reviewer.

## Pitfall classes

These are general. Find the analogue in your own field.

1. **Scope mismatch.** Two numbers measured over different boundaries are compared as if like-for-like.
2. **Qualifier loss.** Measured, simulated, modelled, emulated, spec, typical, projected or trace-replay results are presented as the same kind of evidence.
3. **Footnote redefinition.** A vendor or paper footnote changes what a headline number means.
4. **Circular or inherited citations.** A headline figure traces back to one weak origin.
5. **Undefined denominators,** and ratios read the wrong way.
6. **Attribution slips:** who said it, where, and whether it was a statement or an expectation.
7. **Secondary or abstract-only reading tagged as primary.**
8. **Framing that cannot separate its own cases,** or that proves too much.
9. **Arithmetic slips:** absolute vs added, percent vs log rates, configuration-built costs, extrapolation direction.
10. **Process errors:** wording you prescribed yourself, stale copies after a canonical change, partial state after an interruption.

## Worked examples

The entries below come from a memory-systems study. Each gives what went wrong, then the check.

## Qualifiers and scope
- **Scope mixing in energy/power.** I/O-only pJ/bit compared against full-access or system figures (e.g., a 3D-bond interface 0.37 pJ/bit vs an HBM2 full access 3.92). → Every energy number carries its scope; never compare across scopes; tabulate scope as a column.
- **Vendor footnotes redefine numbers.** "1,200 W" was GPU power, not package power; DRAM power was a separate bar. → Read the footnote and the chart axes, not just the headline; view the slide image.
- **Measured vs spec vs modelled vs simulated vs emulated vs typical.** A latency adder from a spec estimate quoted as measured; a technology-overview figure (TPP Fig. 2) treated as a measurement; emulated results called "pre-production hardware"; simulated savings (Pond) presented as measured. → Tag each number with how it was obtained, in the sentence, not only in the footer.
- **"Production" vs trace replay.** A system deployed in production whose reported gain comes from trace replay. → Say which.
- **Per-direction vs total bandwidth; half-duplex buses.** Serial links are per direction; DDR/HBM buses share read+write. → State the convention once and apply it.
- **Idle vs loaded latency; peak vs sustained bandwidth.** → Label every latency and bandwidth.
- **Batch-1 numbers.** "~1 FLOP/B decode" and "0.3% of GPU peak" are batch-1; batching changes intensity. → State the operating point.

## Sources and citations
- **Circular citation chains.** "Memory is 50% of server cost" traced back through two papers to one trade-press article; a later model simply assumed it. → Follow a headline number to its origin before using it.
- **Undefined denominators.** A "9.8–80.3% of local DRAM bandwidth" ratio whose denominator the paper never defines was mis-explained twice. → If the paper does not define it, say so; don't supply an interpretation.
- **Attribution slips.** TMTS is Google's, not Meta's; a quote attributed to the wrong edition of remarks; Micron's ">4:1" is an expectation. → Re-check who said what, where, and whether it was stated or expected.
- **Reporter paraphrase as quote.** → Mark paraphrases.
- **Chart reads as data.** Values read from vendor charts are approximate (±5–10%); say "read from chart". Use two independent reads for anything plotted.
- **Secondary via notes tagged [P].** A source seen only through notes or another paper is [S via notes], not [P].
- **Abstract-only or intro-only reads.** A claim from an abstract/intro is not a full read. → Fetch the PDF (arXiv usually works) or mark FULL TEXT NEEDED.

## Arithmetic and framing
- **Conflating two axes.** Arithmetic intensity (FLOP per byte moved) vs access density (GB/s demanded per GB stored) are different; one cannot stand in for the other.
- **"Fixed ratio" / single-axis stories.** A unifying variable that cannot separate the cases it claims to explain (two tiers at the same density but different $/GB). → Test the framing against your own table.
- **Absolute vs added latency.** 155–180 ns absolute ≠ +155–180 ns. "182% of local" ≠ "+182%".
- **Ratios of rates.** A slowdown "~2.5×" from percent declines differs from log-rate ratios (2.7–3.1×); state which.
- **Extrapolations.** Label direction and assumptions ("on trend" vs "at constant pJ/bit"); give a range when the regression direction matters.
- **Configuration-built costs.** An "all-in cost" built on a one-controller configuration while the cited system uses two. → Rebuild from the cited system's actual configuration.
- **Arguments that prove too much.** "Distance is a proxy" also applies to the far tier (its cost is hops, not metres); apply your argument to both sides.
- **Causation from correlation.** Supply shortage → adoption: designs predated the shortage; call it an amplifier unless a primary source states the causal link.

## Process
- **Orchestrator-introduced errors.** Prescribed wording in a decisions file ("moves off DDR") was wrong for two of three cited systems. → Your own decisions get reviewed too; fresh reviewers should read them.
- **Stale copies.** Data files fixed after a report embedded them; synthesis lagging the deck. → After any canonical change, grep every artifact; run an embed/consistency check.
- **Partial-revision state after interruption.** → Audit on-disk state against the checklist before relaunching.
