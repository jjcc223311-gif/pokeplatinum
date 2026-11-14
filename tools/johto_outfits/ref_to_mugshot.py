import sys
import numpy as np
from PIL import Image
from collections import deque
ref=Image.open(sys.argv[1]).convert('RGB');cx,top,cw=map(int,sys.argv[2:5]);out=sys.argv[5]
ch=cw*64//96
a=np.array(ref).astype(int)
crop=a[top:top+ch,cx-cw//2:cx-cw//2+cw]
bg=np.array([244,240,238]);near=(np.abs(crop-bg).sum(2))<=24
h,w=near.shape;seen=np.zeros_like(near);dq=deque()
for x in range(w):
    if near[0,x]: seen[0,x]=1;dq.append((0,x))
for y in range(h):
    for x in (0,w-1):
        if near[y,x] and not seen[y,x]: seen[y,x]=1;dq.append((y,x))
while dq:
    y,x=dq.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=y+dy,x+dx
        if 0<=ny<h and 0<=nx<w and near[ny,nx] and not seen[ny,nx]: seen[ny,nx]=1;dq.append((ny,nx))
alpha=(1-seen).astype(np.uint8)*255
rgba=np.dstack([crop.astype(np.uint8),alpha]).astype(float);rgba[...,:3]*=rgba[...,3:4]/255
small=np.array(Image.fromarray(rgba.astype(np.uint8),'RGBA').resize((96,64),Image.LANCZOS)).astype(float)
al=small[...,3];rgb=np.where(al[...,None]>0,small[...,:3]*255/np.maximum(al[...,None],1),0).clip(0,255)
op=al>175
sel=Image.fromarray(rgb[op].astype(np.uint8)[None],'RGB').quantize(colors=14,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE,kmeans=8)
qi=np.array(Image.fromarray(rgb.astype(np.uint8),'RGB').quantize(palette=sel,dither=Image.Dither.NONE))
canvas=np.where(op,qi+1,0).astype(np.uint8)
sil=canvas>0;edge=np.zeros_like(sil)
for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): edge|=np.roll(sil,(dy,dx),(0,1))
edge[0,:]=edge[0,:]&sil[1,:];edge[-1,:]=edge[-1,:]&sil[-2,:];edge[:,0]=edge[:,0]&sil[:,1];edge[:,-1]=edge[:,-1]&sil[:,-2]
edge&=~sil;edge[-1,:]=False;canvas[edge]=15
qp=sel.getpalette()[:42]
pal=[200,192,160]+qp+[24,24,32]
img=Image.fromarray(canvas,'P');img.putpalette(pal+[0]*(768-len(pal)));img.save(out)
img.convert('RGB').resize((384,256),Image.NEAREST).save(out.replace('.png','_prev.png'))
