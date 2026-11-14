import sys;sys.path.insert(0,'/home/claude/ow')
from common import *
import lucas_tmpl as T
SRC='/home/claude/pokeplatinum/res/graphics/field_sprites/player/'
BERET=(1,2)
def beret_box(fr,rows=range(0,19)):
    pts=[(x,y) for y in rows for x in range(32) if fr[y][x] in BERET]
    if not pts: return None
    return min(y for x,y in pts), min(x for x,y in pts), max(x for x,y in pts)
def mirror_t(t,x0):
    w=len(t[2][0]) if False else len(t[0])
    return [r[::-1] for r in t], 32-x0-w
def head(fr,facing,ref):
    """ref: (top,xmin,xmax) of the beret in the base frame the template was drawn on."""
    key={'up':'UP','down':'DOWN','left':'LEFT','right':'LEFT'}[facing]
    x0,y0,t=getattr(T,key)
    t=[r.replace(' ','.') for r in t]
    rtop,rxmin,rxmax=ref[key]
    if facing=='right':
        t=[r[::-1] for r in t]; x0=32-x0-len(t[0]); rxmin,rxmax=31-rxmax,31-rxmin
    b=beret_box(fr)
    dx=dy=0
    if b:
        dy=b[0]-rtop; dx=round(((b[1]+b[2])-(rxmin+rxmax))/2)
    out=[r[:] for r in fr]
    # clear old beret and its band in the head area
    if b:
        for y in range(0,b[0]+12):
            for x in range(32):
                if out[y][x] in BERET: out[y][x]=0
    return apply(out,t,x0+dx,y0+dy),(dx,dy)

NEWPAL={1:(206,170,116),2:(64,64,78),3:(140,96,64)}
def body(fr,facing,dy):
    out=[r[:] for r in fr]
    top=22+dy
    for y in range(top,32):
        for x in range(32):
            v=out[y][x]
            if v==8: out[y][x]=2
            elif v==5: out[y][x]=6
            if facing=='down' and y<top+4 and 12<=x<=19 and fr[y][x] in (5,6,8,2): out[y][x]=2
    for y in range(top+2,top+4):
        for x in range(32):
            if fr[y][x]==1 and any(0<=x+a<32 and fr[y][x+a]==11 for a in (-1,1)): out[y][x]=7
    for y in range(top+5,32):
        for x in range(32):
            if out[y][x]==7: out[y][x]=1
            elif out[y][x]==10: out[y][x]=3 if y==top+5 else 7
    return out
def newpal(pal):
    p=list(pal)
    for i,c in NEWPAL.items(): p[i]=c
    return p
