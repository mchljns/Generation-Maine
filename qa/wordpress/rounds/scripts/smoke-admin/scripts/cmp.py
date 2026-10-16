# cmp.py <mine> <theirs>: compare two JSON outputs after normalizing ports, instance names, nonces, timestamps and update notices
import json, re, sys
def load(p):
    s = open(p).read(); i = min([x for x in (s.find('{'), s.find('[')) if x >= 0]); s = s[i:]
    end = max(s.rfind('}'), s.rfind(']')); return s[:end + 1]
def norm(s):
    s = re.sub(r'89[0-9]{2}', 'PORT', s); s = re.sub(r'\b(a71|a65|sa71|sa65|admin71|admin65)\b', 'INST', s)
    s = s.replace('WordPress 7.1.3 is available! Please update now.', 'UPD')
    s = re.sub(r'"(_wpnonce|nonce|gm_creator_nonce)=?[0-9a-f]{10}"', '"NONCE"', s); s = re.sub(r'[0-9a-f]{10}', lambda m: m.group(0) if not re.match(r'^[0-9]+$', m.group(0)) else m.group(0), s)
    return json.loads(s)
a = norm(load(sys.argv[1])); b = norm(load(sys.argv[2]))
diffs = []
def walk(x, y, path):
    if type(x) != type(y): diffs.append((path, x, y)); return
    if isinstance(x, dict):
        for k in sorted(set(x) | set(y)): walk(x.get(k), y.get(k), path + '.' + str(k))
    elif isinstance(x, list):
        if len(x) != len(y): diffs.append((path + ' len', len(x), len(y)))
        for i, (p, q) in enumerate(zip(x, y)): walk(p, q, path + '[%d]' % i)
    elif x != y: diffs.append((path, x, y))
walk(a, b, '')
print(sys.argv[1].split('/')[-1], 'vs', sys.argv[2].split('/')[-1], ':', len(diffs), 'differences')
for d in diffs[:40]: print('  ', d[0], '| mine:', json.dumps(d[1])[:160], '| r4:', json.dumps(d[2])[:160])
