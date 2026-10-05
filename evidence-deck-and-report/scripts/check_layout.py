#!/usr/bin/env python3
"""Measure footer-rule position and clearance on every rendered slide, and build a contact sheet.

Run after `assemble.py --shots`. Assumes 1280x720 slides rendered on a 1340x760 canvas with
the deck.css footer rule (colour ~#e3e6ea).
Usage: python3 check_layout.py [--root DIR] [--min-clear 12]
Prints: slide, footer-rule y, clearance (px between lowest body content and the rule).
Flags slides whose rule is not at the deck's modal y (footer overflowed to an extra line) or
whose clearance is below --min-clear. Writes shots/contact.png (2 columns).
"""
import sys as _s
if "-h" in _s.argv or "--help" in _s.argv:
    print(__doc__); _s.exit(0)
import sys, os, glob, pathlib, collections
from PIL import Image
import numpy as np

def arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

root = pathlib.Path(arg("--root", os.environ.get("DECK_ROOT", "."))).resolve()
min_clear = int(arg("--min-clear", 12))
shots = sorted(glob.glob(str(root / "shots" / "s[0-9][0-9].png")))
rows = []
for f in shots:
    im = np.asarray(Image.open(f).convert("L"))
    ys = [y for y in range(560, im.shape[0] - 1) if (np.abs(im[y, 100:1240].astype(int) - 227) < 6).mean() > 0.9]
    if not ys:
        rows.append((f, None, None)); continue
    rule = ys[0]
    content = [y for y in range(400, rule) if (im[y, 92:1250] < 235).sum() > 3]
    rows.append((f, rule, rule - max(content) if content else None))
modal = collections.Counter(r[1] for r in rows if r[1]).most_common(1)[0][0] if rows else None
bad = 0
for f, rule, clear in rows:
    flags = []
    if rule is None: flags.append("NO RULE FOUND")
    elif rule != modal: flags.append(f"rule at {rule}, deck modal {modal}: footer wrapped to an extra line")
    if clear is not None and clear < min_clear: flags.append(f"clearance {clear}px < {min_clear}px")
    bad += bool(flags)
    print(f"{pathlib.Path(f).stem}: rule={rule} clear={clear} {'  <-- ' + '; '.join(flags) if flags else ''}")
if shots:
    ims = [Image.open(f).crop((30, 28, 1310, 748)).resize((640, 360)) for f in shots]
    W = Image.new("RGB", (1280, 360 * ((len(ims) + 1) // 2)), "white")
    for k, im in enumerate(ims):
        W.paste(im, ((k % 2) * 640, (k // 2) * 360))
    W.save(root / "shots" / "contact.png")
    print("contact sheet:", root / "shots" / "contact.png")
sys.exit(1 if bad else 0)
