#!/usr/bin/env python3
# Summarize a gest.mjs / gestx.mjs log: one-card runs, mismatches, and every against-the-swipe move the page script made,
# split into the VIS-N05 half-screen corrections the fixer kept (half swipe at 768x1024 or 844x390: back from 9 or 8,
# forward from 6 or 7) and anything else. usage: gestsum.py <log>...
import re, sys
for f in sys.argv[1:]:
    s = open(f).read().splitlines()
    one = [l for l in s if 'ONE-CARD' in l]
    tot = [l for l in s if l.startswith('TOTAL')]
    mism = [l for l in s if 'MISMATCH' in l]
    allowed, other, browser_big = [], [], []
    for l in s:
        m = re.match(r'(\w+) (\d+x\d+) (BACK|FWD ) (\w+)\s+from (\d+)@\d+: .*against-gesture (\d+)px', l)
        if not m: continue
        tgt, size, d, kind, frm, px = m.groups(); frm = int(frm); px = int(px)
        if 'BY SCRIPT' in l:
            ok = kind == 'half' and size in ('768x1024', '844x390') and ((d == 'BACK' and frm in (8, 9)) or (d.strip() == 'FWD' and frm in (6, 7)))
            (allowed if ok else other).append(l[:220])
        elif px > 160:
            browser_big.append(l[:220])
    print(f'## {f}')
    for l in one: print('  ' + l[:200])
    for l in tot: print('  ' + l)
    print(f'  mismatches {len(mism)}; script corrections VIS-N05 {len(allowed)}; OTHER script moves against the swipe {len(other)}; browser moves >160px {len(browser_big)}')
    for l in mism + other + browser_big: print('    ' + l)
