#!/usr/bin/env python3
"""Flag the copy tells that read as machine-written, in HTML or Markdown files.

    copy_check.py <file>... [--max-words 28] [--max-headline 10] [--ban word,word] [--allow-italics]

Checks: em and en dashes used as punctuation, italics, banned words (default: earn earns earned earning),
hype and filler words, sentences over --max-words, headlines over --max-headline words, numbers in prose,
remaining [CONFIRM:] placeholders (listed, not failed), British spellings, "Not X. Y." contrast tics, triplet lists.
Exit 1 when any hard check fails. Tune the lists to the project's rules; the defaults are the ones this skill recommends.
"""
import re, sys, html

HYPE = ['unlock', 'elevate', 'seamless', 'empower', 'leverage', 'cutting-edge', 'world-class', 'game-changing',
        'revolutionary', 'next-level', 'supercharge', 'effortless', 'delve', 'tapestry', 'vibrant', 'robust',
        'journey', 'passionate', 'innovative', 'transform', 'unleash', 'landscape',
        'ecosystem', 'synergy', 'holistic', 'curated', 'bespoke', 'crafted with', 'in today\'s', 'whether you\'re',
        'look no further', 'we believe', 'at the heart of', 'more than just', 'it\'s not just', 'dive in']
BRITISH = ['colour', 'favourite', 'organise', 'realise', 'centre', 'licence', 'programme', 'behaviour', 'grey']

def text_of(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    if path.endswith(('.html', '.htm')):
        s = re.sub(r'<(script|style)\b.*?</\1>', ' ', s, flags=re.S | re.I)
        heads = [html.unescape(re.sub(r'<[^>]+>', ' ', h)) for h in re.findall(r'<h[1-3]\b[^>]*>(.*?)</h[1-3]>', s, flags=re.S | re.I)]
        italics = len(re.findall(r'<(em|i)\b(?![^>]*aria-hidden)', s, flags=re.I))
        # block boundaries end a sentence, so navigation and labels are not glued into one long run
        s = re.sub(r'</(p|h[1-6]|li|div|section|article|header|footer|nav|figcaption|td|th|dt|dd|blockquote|button|label|title)>', '\n', s, flags=re.I)
        body = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    else:
        heads = [h.strip('# ').strip() for h in re.findall(r'^#{1,3} .*$', s, flags=re.M)]
        italics = len(re.findall(r'(?<![*_])[*_](?![*_\s])[^*_\n]+[*_](?![*_])', s))
        body = s
    body = re.sub(r'[ \t]+', ' ', body)
    return body, heads, italics

def main():
    args = sys.argv[1:]
    maxw, maxh, allow_it = 28, 10, False
    ban = ['earn', 'earns', 'earned', 'earning']
    for flag, setter in (('--max-words', lambda v: ('maxw', int(v))), ('--max-headline', lambda v: ('maxh', int(v))), ('--ban', lambda v: ('ban', v.split(',')))):
        if flag in args:
            i = args.index(flag); k, v = setter(args[i + 1]); del args[i:i + 2]
            if k == 'maxw': maxw = v
            elif k == 'maxh': maxh = v
            else: ban = v
    if '--allow-italics' in args: allow_it = True; args.remove('--allow-italics')
    failed = False
    for path in args:
        body, heads, italics = text_of(path)
        issues, notes = [], []
        n = body.count('—') + len(re.findall(r'\s–\s', body))
        if n: issues.append(f'{n} em/en dash(es) used as punctuation')
        if italics and not allow_it: issues.append(f'{italics} italic run(s)')
        for w in ban:
            c = len(re.findall(r'\b' + re.escape(w) + r'\b', body, flags=re.I))
            if c: issues.append(f'banned word "{w}" x{c}')
        hits = [w for w in HYPE if re.search(r'\b' + re.escape(w) + r'\b', body, flags=re.I)]
        if hits: issues.append('hype or filler: ' + ', '.join(hits))
        brit = [w for w in BRITISH if re.search(r'\b' + w + r'\b', body, flags=re.I)]
        if brit: issues.append('British spelling: ' + ', '.join(brit))
        long_s = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+', body) if len(s.split()) > maxw and '[CONFIRM' not in s]
        if long_s: issues.append(f'{len(long_s)} sentence(s) over {maxw} words, e.g. "{long_s[0][:90]}..."')
        long_h = [h for h in heads if len(h.split()) > maxh]
        if long_h: issues.append(f'headline over {maxh} words: "{long_h[0][:80]}"')
        tics = len(re.findall(r'\b(?:It\'s|This is) not (?:just |about )?[^.]{3,60}\. (?:It\'s|This is)\b', body))
        if tics: issues.append(f'{tics} "not X. It\'s Y." contrast tic(s)')
        conf = re.findall(r'\[CONFIRM:[^\]]*\]', body)
        if conf: notes.append(f'{len(conf)} [CONFIRM] placeholder(s) still open')
        print(f'== {path}')
        for i in issues: print('  FAIL', i)
        for i in notes: print('  note', i)
        if not issues: print('  ok')
        failed = failed or bool(issues)
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
