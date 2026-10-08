#!/usr/bin/env python3
"""Diff the visible text of two built pages, so copy differences between variants are intentional.

    textdiff.py a/index.html b/index.html

Strips script, style and svg, drops tags, unescapes entities, splits on block boundaries and prints a
unified diff of the resulting lines. Identical visible text prints nothing and exits 0.
"""
import difflib, html, re, sys

def visible(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'<(script|style|svg|noscript)\b.*?</\1>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'</(p|h[1-6]|li|div|section|article|header|footer|nav|figcaption|td|th|dt|dd|blockquote|button|label|title|a|span)>', '\n', s, flags=re.I)
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    lines = [re.sub(r'\s+', ' ', l).strip() for l in s.split('\n')]
    return [l for l in lines if l]

def main():
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    a, b = visible(sys.argv[1]), visible(sys.argv[2])
    d = list(difflib.unified_diff(a, b, fromfile=sys.argv[1], tofile=sys.argv[2], lineterm='', n=0))
    for line in d: print(line)
    changed = sum(1 for l in d if l[:1] in '+-' and not l.startswith(('+++', '---')))
    print(f'{changed} changed line(s)' if changed else 'visible text identical')
    sys.exit(1 if changed else 0)

if __name__ == '__main__':
    main()
