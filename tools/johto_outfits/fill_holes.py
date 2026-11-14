import sys, numpy as np
from PIL import Image
from collections import deque, Counter
def holes(fr):
    H,W=fr.shape; tr=(fr==0); seen=np.zeros(tr.shape,bool); dq=deque()
    for y in range(H):
        for x in range(W):
            if (y in (0,H-1) or x in (0,W-1)) and tr[y,x]: seen[y,x]=1; dq.append((y,x))
    while dq:
        y,x=dq.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and tr[ny,nx] and not seen[ny,nx]: seen[ny,nx]=1; dq.append((ny,nx))
    return tr & ~seen
def lum(p,i): return sum(p[3*i:3*i+3])
def fill(fr,pal):
    h=holes(fr); H,W=fr.shape; seen=np.zeros_like(h); n=0
    used=[i for i in np.unique(fr) if i not in (0,255)]
    dark=min(used,key=lambda i:lum(pal,i))
    for sy,sx in zip(*np.nonzero(h)):
        if seen[sy,sx]: continue
        comp=[];dq=deque([(sy,sx)]);seen[sy,sx]=1;border=Counter()
        while dq:
            y,x=dq.popleft();comp.append((y,x))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=y+dy,x+dx
                if not(0<=ny<H and 0<=nx<W): continue
                if h[ny,nx]:
                    if not seen[ny,nx]: seen[ny,nx]=1;dq.append((ny,nx))
                elif fr[ny,nx] not in (0,255): border[fr[ny,nx]]+=1
        nd=Counter({k:v for k,v in border.items() if k!=dark and lum(pal,k)>=300}) or Counter({k:v for k,v in border.items() if k!=dark}) or border
        c=nd.most_common(1)[0][0]
        for y,x in comp: fr[y,x]=c
        n+=len(comp)
    return n
def frames(a,kind):
    if kind=='sep':
        seps=[y for y in range(a.shape[0]) if (a[y]==255).all()]
        st=[0]+[s+1 for s in seps]; en=seps+[a.shape[0]]
        return [(s,e,0,a.shape[1]) for s,e in zip(st,en)]
    if kind=='half': return [(0,a.shape[0],0,80),(0,a.shape[0],80,160)]
    if kind=='ow':
        H,W=a.shape; return [(y,y+32,x,x+32) for y in range(0,H,32) for x in range(0,W,32)]
for rel,kind in [('rival/front.png','sep'),('rival/back.png','sep'),('rival/front_scan.png','half'),('rival/back_scan.png','half'),('field_sprites/npc/barry.png','ow')]:
    p='res/johto_outfits/'+rel; im=Image.open(p); a=np.array(im); pal=im.getpalette()
    before=a.copy(); tot=[]
    for y0,y1,x0,x1 in frames(a,kind):
        fr=a[y0:y1,x0:x1]; tot.append(fill(fr,pal))
    after=[int(holes(a[y0:y1,x0:x1]).sum()) for y0,y1,x0,x1 in frames(a,kind)]
    out=Image.fromarray(a,'P'); out.putpalette(pal)
    if 'transparency' in im.info: out.info['transparency']=im.info['transparency']
    out.save(p, transparency=im.info.get('transparency',0)) if 'transparency' in im.info else out.save(p)
    print(rel,'filled',tot,'remaining',sum(after))
