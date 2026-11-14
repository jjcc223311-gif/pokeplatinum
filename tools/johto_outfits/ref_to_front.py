import sys
import numpy as np
from PIL import Image
ref=Image.open(sys.argv[1]).convert('RGB');x0,x1,y0,y1=map(int,sys.argv[2:6]);H=int(sys.argv[6]);out=sys.argv[7]
a=np.array(ref).astype(int);bg=np.array([244,240,238])
crop=a[y0:y1+1,x0:x1+1]
near=(np.abs(crop-bg).sum(2))<=24
# flood fill background from the crop border so white clothing stays
from collections import deque
h,w=near.shape;seen=np.zeros_like(near);dq=deque()
for x in range(w):
    for y in (0,h-1):
        if near[y,x]: seen[y,x]=1;dq.append((y,x))
for y in range(h):
    for x in (0,w-1):
        if near[y,x] and not seen[y,x]: seen[y,x]=1;dq.append((y,x))
while dq:
    y,x=dq.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=y+dy,x+dx
        if 0<=ny<h and 0<=nx<w and near[ny,nx] and not seen[ny,nx]: seen[ny,nx]=1;dq.append((ny,nx))
alpha=(1-seen).astype(np.uint8)*255
rgba=np.dstack([crop.astype(np.uint8),alpha])
im=Image.fromarray(rgba,'RGBA')
s=H/im.height;W=max(1,round(im.width*s))
# premultiplied downscale
pm=np.array(im).astype(float);pm[...,:3]*=pm[...,3:4]/255
small=Image.fromarray(pm.astype(np.uint8),'RGBA').resize((W,H),Image.LANCZOS)
sa=np.array(small).astype(float)
al=sa[...,3]
rgb=np.where(al[...,None]>0,sa[...,:3]*255/np.maximum(al[...,None],1),0).clip(0,255)
opaque=al>175
# quantize opaque pixels to 15 colours
pix=Image.fromarray(rgb.astype(np.uint8),'RGB')
sel=Image.fromarray(rgb[opaque].astype(np.uint8)[None,:,:],'RGB')
qs=sel.quantize(colors=14,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE,kmeans=8)
q=pix.quantize(palette=qs,dither=Image.Dither.NONE)
qp=q.getpalette()[:42];qi=np.array(q)
# canvas 80x80, bottom aligned, centred
canvas=np.zeros((80,80),np.uint8)
ox=(80-W)//2;oy=80-H-2
for y in range(H):
    for x in range(W):
        if opaque[y,x] and 0<=ox+x<80: canvas[oy+y,ox+x]=qi[y,x]+1
# outline: transparent pixel next to opaque -> darkest colour, only where original had dark edge
cols=[tuple(qp[3*i:3*i+3]) for i in range(14)]+[(24,24,32)]
dark=15
# 1px outline around the silhouette
sil=canvas>0
edge=np.zeros_like(sil)
for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    edge|=np.roll(sil,(dy,dx),(0,1))
edge[0,:]=edge[0,:]&sil[1,:];edge[-1,:]=edge[-1,:]&sil[-2,:];edge[:,0]=edge[:,0]&sil[:,1];edge[:,-1]=edge[:,-1]&sil[:,-2]
edge&=~sil
canvas[edge]=dark
pal=[(255,0,255)]+cols
img=Image.fromarray(canvas,'P');flat=[]
for c in pal: flat+=list(c)
img.putpalette(flat+[0]*(768-len(flat)))
img.save(out)
prev=img.convert('RGBA');d=np.array(prev);d[canvas==0]=[120,160,120,255]
Image.fromarray(d).resize((320,320),Image.NEAREST).save(out.replace('.png','_prev.png'))
