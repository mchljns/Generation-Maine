import json,sys
d=json.load(open(sys.argv[1]))
for k in ['front1440','front390','editor']:
    v=d[k]
    print('=====',k)
    print(' title',v['title'])
    print(' intro',v['introP'])
    for b in v['buttons']:
        print(' buttons',b['display'],b['flexWrap'],b['justifyContent'],b['gap'],b['box'])
        for i in b['items']: print('   ',i)
    print(' columns',v['columns'])
    for r in ['row','rowTop','stack','grid']: print(' ',r,v[r])
    print(' gallery',v['gallery'])
    print(' quote',v['quote'])
    print(' hr',v['hr'])
    print(' table',v['table'])
    print(' h2',v['h2'])
    print(' overflow',v['overflow'])
for k in ['axe1440','axe390','focus','hover','hoverOutline','editorIframe','renderingMode','editorRoot']: print(k, d.get(k))
