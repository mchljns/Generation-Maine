# sum-details.py <V> <run>: summarize the Creator details results and compare them with the fixer's (fix4-admin g/d/f runs)
import json, sys, re
V, R = sys.argv[1], sys.argv[2]; L = '/tmp/claude-0/wptest/work/smoke-admin/logs/'; F = '/tmp/claude-0/wptest/work/fix4-admin/logs/'
ok = True
def chk(name, cond, detail=''):
    global ok; ok = ok and cond; print(('PASS ' if cond else 'FAIL ') + name + (' | ' + detail if detail else ''))
d = json.load(open(L + 'dirty4-%s%s.json' % (R, V))); f = json.load(open(F + 'dirty4-g%s.json' % V))
for k, v in d['ctrlS'].items():
    stored_ok = v['stored'] != v['was'] and 'missing' not in v['stored'] if k not in ('placeholder', 'removeClip') else (v['stored'] in ('(missing: exit 1)', '', '0'))
    chk('ctrlS ' + k, v['dirtyBeforeCtrlS'] and len(v['requests']) == 2 and not v['dirtyAfter'] and v['author'] == '2' and stored_ok, 'was %s stored %s req %d' % (v['was'][:30], v['stored'][:40], len(v['requests'])))
for k, v in d['leave'].items():
    chk('leave ' + k, v['dirty'] and v['dialogs'] == ['beforeunload'] and v['nav'] == 'stayed' and v['storedUnchanged'], json.dumps(v)[:120])
u, fu = d['undo'], f['undo']
chk('undo button greyed after a box edit (as fixer)', u['undoEnabled'] == fu['undoEnabled'] == False, 'mine %s fixer %s' % (u['undoEnabled'], fu['undoEnabled']))
chk('after Undo: box == store, dirty', u['afterUndo']['dirty'] and u['afterUndo']['box'] == u['afterUndo']['storeMeta'], json.dumps(u['afterUndo']))
chk('Ctrl+S after Undo stores the box text', u['afterCtrlS']['stored'] == u['afterUndo']['box'] and len(u['afterCtrlS']['requests']) == 2, json.dumps(u['afterCtrlS'])[:200])
chk('Save button after Undo stores box text', u['afterButton']['stored'] == u['afterButton']['box'] and len(u['afterButton']['requests']) == 2, json.dumps(u['afterButton'])[:200])
u2 = d['undo2']
chk('undo2: box == store after Undo clicks, still dirty', u2['afterUndos']['dirty'] and u2['afterUndos']['box'] == u2['afterUndos']['storeMeta'], json.dumps(u2['afterUndos']))
chk('undo2: Ctrl+S stores box text', u2['ctrlS']['stored'] == u2['afterUndos']['box'] and len(u2['ctrlS']['requests']) == 2, json.dumps(u2['ctrlS'])[:200])
chk('author kept, no page errors', d['authorKept'] and not d['errors'], json.dumps({'before': d['before'], 'after': d['after'], 'errors': d['errors']}))
def j(p):
    s = open(p).read(); s = s[s.index('{'):]; return json.loads(s[:s.rindex('}') + 1])
c = j(L + 'ctrlz-%s%s.txt' % (R, V)); st = {x['label']: x for x in c['steps']}
chk('ctrlz: one Ctrl+Z restores field and store, not dirty', st['ctrlz1']['box'] == st['open']['box'] == st['ctrlz1']['store'] and not st['ctrlz1']['dirty'], json.dumps(st['ctrlz1']))
chk('ctrlz: Ctrl+Shift+Z brings the typing back, dirty', st['redo1']['box'] == st['typed']['box'] == st['redo1']['store'] and st['redo1']['dirty'], json.dumps(st['redo1']))
chk('ctrlz: no editor undo steps from the box', not any(x['hasUndo'] for x in c['steps']) and not c['errs'], '')
us = j(L + 'undoshot-%s%s.txt' % (R, V))
chk('undoshot2: box == store, dirty, leave warns, nothing stored', us['dirty'] and us['box'] == us['store'] and us['leaveDialogs'] == ['beforeunload'] and us['storedAfterLeave'] == us['saved'], json.dumps(us)[:300])
um = j(L + 'undomix-%s%s.txt' % (R, V)); fm = j(F + 'undomix-fix%s.txt' % V)
chk('undomix: box and store agree at every step', all(x['agree'] for x in um['steps']), '')
mine = [(x['label'], x['dirty'], x['title'].replace(um['saved']['title'], 'T0'), x['box'].replace(um['saved']['town'], 'H0'), x['storePlace'] - int(um['saved']['place']), x['hasUndo'], x['hasRedo']) for x in um['steps']]
fix = [(x['label'], x['dirty'], x['title'].replace(fm['saved']['title'], 'T0'), x['box'].replace(fm['saved']['town'], 'H0'), x['storePlace'] - int(fm['saved']['place']), x['hasUndo'], x['hasRedo']) for x in fm['steps']]
# Place 11 then Undo writes back intermediate values typed digit by digit: compare relative only where it was relative in the fixer's run
diff = [(a, b) for a, b in zip(mine, fix) if a != b and not ('place typed' in a[0] or a[0].startswith('after Undo clicked'))]
chk('undomix: same sequence as fixer (title undo/redo, box kept, Place undone)', not diff and um['after']['town'] == um['saved']['town'] + ' Mix' and um['after']['author'] == '2', json.dumps(diff)[:300] + ' after ' + json.dumps(um['after']))
dd = json.load(open(L + 'dirty-d%s%s.json' % (R, V)))
chk('dirty.mjs: clean after clicks, clean after typing back, cleaned save stays clean', dd['cleanAfterClicks'] and dd['cleanAfterTypingBack'] and dd['cleanAfterCleanedSave'] and dd['dirtyAfterTyping'], '')
steps_ok = all(v['dirtyBeforeCtrlS'] and len(v['requests']) == 2 for v in dd['steps'].values())
chk('dirty.mjs: every step dirty before Ctrl+S and both requests sent', steps_ok, ','.join(k for k, v in dd['steps'].items() if not (v['dirtyBeforeCtrlS'] and len(v['requests']) == 2)))
chk('dirty.mjs: author kept, place saved, leave warns', dd['after']['author'] == dd['before']['author'] and dd['leave']['dialogs'][:1] == ['beforeunload'] and not dd['errors'], json.dumps({'before': dd['before'], 'after': dd['after'], 'leave': dd['leave']})[:300])
g = json.load(open(L + 'goneclip-g%s%s.json' % (R, V)))
chk('goneclip: clean on load, save clears stale id', g['cleanAfterClicks'] and g['after']['clip'] == '0' and g['boxClipField'] == '0' and not g['errors'], json.dumps(g))
cc = json.load(open(L + 'contribctrls-c%s%s.json' % (R, V)))
chk('contribctrls: draft saved with Hometown, link, Handle; author stays contrib1', cc['first']['status'] == 'draft' and cc['first']['hometown'] == 'Bath' and cc['first']['link'].startswith('https://example.org/contrib') and cc['first']['author'] == '4' and cc['second']['handle'].startswith('@contrib') and cc['second']['author'] == '4' and cc['dirty'] and all(r.startswith(('200', '302')) for r in cc['first']['requests'] + cc['second']['requests']), json.dumps({k: cc[k] for k in ('first', 'second', 'dirty')})[:400])
print('ALL PASS' if ok else 'SOME FAIL')
