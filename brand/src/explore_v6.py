"""Brandmark explorations for v6, kept as the record of routes tested and dropped.

Run: python3 brand/src/explore_v6.py  (writes brand/v6/explorations.html)
"""
import sys
SP,PI,BI,MG='#104836','#0B2B21','#F4F0E6','#EFB443'
def arch(x,w,top,bot,fill):
    r=w/2
    return '<path fill="%s" d="M%s %s V%s A%s %s 0 0 1 %s %s V%s Z"/>'%(fill,x,bot,top+r,r,r,x+w,top+r,bot)
C={}
C['Floating arch: reads as a headstone on light']=lambda bg,fg,mk: arch(56,88,40,172,fg)+'<circle cx="100" cy="84" r="20" fill="%s"/>'%mk
C['Dot low: reads as a doorknob']=lambda bg,fg,mk: arch(56,88,40,172,fg)+'<circle cx="100" cy="126" r="20" fill="%s"/>'%mk
C['On a ground line: a headstone']=lambda bg,fg,mk: arch(62,76,36,160,fg)+'<rect x="36" y="160" width="128" height="12" fill="%s"/>'%fg+'<circle cx="100" cy="112" r="18" fill="%s"/>'%mk
C['Caption: an app toggle']=lambda bg,fg,mk: '<rect x="28" y="62" width="144" height="36" rx="18" fill="%s"/><rect x="28" y="106" width="98" height="36" rx="18" fill="%s"/>'%(fg,fg)+'<circle cx="46" cy="80" r="10" fill="%s"/>'%mk
C['Dot and stem: the info icon']=lambda bg,fg,mk: '<circle cx="100" cy="56" r="24" fill="%s"/><rect x="80" y="92" width="40" height="80" rx="20" fill="%s"/>'%(mk,fg)
def tile(fn,bg,fg,mk,px,rx=0.22):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="%d" height="%d" style="border-radius:%d%%"><rect width="200" height="200" fill="%s"/>%s</svg>'%(px,px,rx*100,bg,fn(bg,fg,mk))
rows=''
for name,fn in C.items():
    cells=''.join(tile(fn,SP,BI,MG,p) for p in (180,64,32,16))+''.join(tile(fn,BI,SP,MG,p) for p in (180,32))+tile(fn,MG,SP,BI,64)+'<span style="border-radius:50%;overflow:hidden;display:inline-block;width:64px;height:64px">'+tile(fn,SP,BI,MG,64,0)+'</span>'
    rows+='<div style="display:flex;gap:18px;align-items:center;margin:16px 0"><b style="width:190px;font:600 14px Arial,sans-serif;color:#1E2621">%s</b>%s</div>'%(name,cells)
open('brand/v6/explorations.html','w').write('<html><body style="background:#F4F0E6;padding:20px;margin:0">%s</body></html>'%rows)
