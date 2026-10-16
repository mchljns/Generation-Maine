# cmpnames.py <mine.json> <fixer.json>: names.mjs results against the fixer's final run
import json, sys, re
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
n = lambda o: json.loads(re.sub(r'127\.0\.0\.1:\d+', 'HOST', json.dumps(o)))
bad = 0
for w in ('w1440', 'w320'):
    for k in sorted(set(a[w]) | set(b[w])):
        x, y = n(a[w].get(k)), n(b[w].get(k))
        if x != y: bad += 1; print('DIFF', w, k, '\n   mine', json.dumps(x)[:400], '\n   fix ', json.dumps(y)[:400])
for k in ('rawWho', 'rawTexturized', 'rawTexturizedSamples'):
    if n(a[k]) != n(b[k]): bad += 1; print('DIFF', k, json.dumps(a[k])[:300], '|', json.dumps(b[k])[:300])
print('made', [(m['title'], m.get('storedHandle')) for m in a['made']])
print('rawTexturized', a['rawTexturized'], a['rawTexturizedSamples']); print('errors', a['errors'])
print('differences', bad)
