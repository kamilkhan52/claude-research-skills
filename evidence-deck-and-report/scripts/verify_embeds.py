#!/usr/bin/env python3
"""Check that every <script type="application/json"> block embedded in an HTML file equals a data file.

Usage: python3 verify_embeds.py page.html data_dir/
Matches blocks to files by parsed-JSON equality (ignores *.b.json second extractions).
Exit code 1 if any block matches no file: the page carries stale data.
"""
import sys as _s
if "-h" in _s.argv or "--help" in _s.argv:
    print(__doc__); _s.exit(0)
import sys, re, json, glob, os
if len(sys.argv) < 3:
    print(__doc__); sys.exit(2)
html, data_dir = sys.argv[1], sys.argv[2]
s = open(html).read()
files = {os.path.basename(f): json.load(open(f)) for f in glob.glob(os.path.join(data_dir, "*.json")) if not f.endswith(".b.json")}
stale = 0
for bid, txt in re.findall(r'<script type="application/json" id="([^"]+)">(.*?)</script>', s, re.S):
    try:
        d = json.loads(txt)
    except Exception as e:
        print(f"{bid}: PARSE ERROR {e}"); stale += 1; continue
    m = [k for k, v in files.items() if v == d]
    print(f"{bid}: {'OK ' + m[0] if m else 'STALE (matches no data file)'}")
    stale += not m
sys.exit(1 if stale else 0)
