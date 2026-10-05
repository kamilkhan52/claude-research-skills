#!/usr/bin/env python3
"""Compare two blind extractions of the same figure data (<id>.json vs <id>.b.json).

Usage: python3 compare_extractions.py data/<id>.json data/<id>.b.json [--key name] [--fields a,b,c] [--tol 0.05]
Rows are matched on --key (default: first string field present in both). Numeric fields are compared
with relative tolerance --tol. Prints matched rows with disagreements, rows found by only one extractor,
and the max relative disagreement. Reconciliation (going back to the source) is a human/agent step;
record the outcome in the A file's extraction.cross_check.
"""
import sys as _s
if "-h" in _s.argv or "--help" in _s.argv:
    print(__doc__); _s.exit(0)
import sys, json
if len(sys.argv) < 3:
    print(__doc__); sys.exit(2)
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default
tol = float(arg("--tol", 0.05))
def rows(d):
    for k in ("rows", "points", "series"):
        if isinstance(d.get(k), list) and d[k] and isinstance(d[k][0], dict):
            return d[k]
    return []
ra, rb = rows(a), rows(b)
key = arg("--key")
if not key and ra:
    key = next((k for k, v in ra[0].items() if isinstance(v, str) and any(k in r for r in rb)), None)
fields = arg("--fields")
fields = fields.split(",") if fields else sorted({k for r in ra for k, v in r.items() if isinstance(v, (int, float)) and not isinstance(v, bool)})
ia = {str(r.get(key)): r for r in ra}; ib = {str(r.get(key)): r for r in rb}
worst = 0.0
for k in sorted(set(ia) & set(ib)):
    diffs = []
    for f in fields:
        x, y = ia[k].get(f), ib[k].get(f)
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            rel = abs(x - y) / max(abs(x), abs(y), 1e-12)
            worst = max(worst, rel)
            if rel > tol: diffs.append(f"{f}: A={x} B={y} ({rel:.1%})")
        elif x != y and (x is not None or y is not None):
            diffs.append(f"{f}: A={x!r} B={y!r}")
    if diffs: print(f"[{k}] " + "; ".join(diffs))
print("only in A:", sorted(set(ia) - set(ib)))
print("only in B:", sorted(set(ib) - set(ia)))
print(f"key={key} fields={fields} max relative disagreement={worst:.1%}")
