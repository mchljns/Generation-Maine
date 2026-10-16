# cmpclip.py <mine> <r4>: compare clip.mjs step results (box state, warning, stored values), with ports and media ids normalized
import json, re, sys
def steps(p):
    out = []
    for l in open(p):
        m = re.match(r'after (.*?): (\{.*\}) \| stored clip_id=(\S*) clip_url=(\S*)', l)
        if m:
            d = json.loads(m.group(2)); n = lambda s: re.sub(r'127\.0\.0\.1:\d+', 'HOST', s or '')
            out.append((n(m.group(1)), 'none' if d['clipId'] in ('0', '') else 'clip:' + d['name'], d['warning'], n(d['link']), d['removeVisible'], 'none' if m.group(3) in ('0', '', '(missing') else 'id', n(m.group(4))))
        elif l.startswith(('  save', '  ctrl+s', 'errors')): out.append((l.strip()[:80],))
    return out
a, b = steps(sys.argv[1]), steps(sys.argv[2]); bad = 0
for i, (x, y) in enumerate(zip(a, b)):
    if x != y: bad += 1; print('DIFF', i, '\n  mine', x, '\n  r4  ', y)
print(sys.argv[1].split('/')[-1], 'steps', len(a), len(b), 'differences', bad + abs(len(a) - len(b)))
for x in a: print('   ', ' | '.join(str(v)[:60] for v in x))
