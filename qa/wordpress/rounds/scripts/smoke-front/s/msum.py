#!/usr/bin/env python3
# Summarize measure.mjs logs (=== WxH then a JSON object) and compare each viewport with a baseline log.
# usage: msum.py <mine> [baseline]
import json, sys, re
def load(f):
    s = open(f).read(); out = {}
    for m in re.finditer(r'^=== (\d+x\d+)\n', s, re.M):
        o, _ = json.JSONDecoder().raw_decode(s, m.end()); out[m.group(1)] = o
    return out
def row(o):
    return {'overflow': o['docOverflowPx'], 'pageH': o['pageHeight'], 'tapUnder44': len(o['tapTargetsUnder44']), 'textOverflow': len(o['textOverflow']),
            'noAlt': len(o['imagesWithoutAlt']), 'under12': len(o['textUnder12px']), 'h1': o['h1Count'], 'fonts': ','.join(o['fonts']),
            'media': o.get('mediaRequestedAtLoad', {}).get('count'), 'errors': len(o.get('errors', []))}
a = load(sys.argv[1]); b = load(sys.argv[2]) if len(sys.argv) > 2 else {}
for vp, o in a.items():
    r = row(o); line = f'{vp}: ' + ' '.join(f'{k}={v}' for k, v in r.items() if k != 'fonts') + f" fonts={r['fonts']}"
    if vp in b:
        rb = row(b[vp]); d = {k: (rb[k], r[k]) for k in r if rb[k] != r[k]}
        line += f'  | vs baseline: {"same" if not d else d}'
        if o['textOverflow'] or o.get('errors'): line += f"  textOverflow={o['textOverflow']} errors={o.get('errors')}"
    print(line)
