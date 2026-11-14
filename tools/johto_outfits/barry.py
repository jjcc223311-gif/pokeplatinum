import sys;sys.path.insert(0,'/home/claude/ow')
from common import *
SRC='/home/claude/pokeplatinum/res/graphics/field_sprites/npc/barry.png'
def convert():
    im,pal=load(SRC)
    n=im.size[1]//32
    frames=[frame(im,k) for k in range(n)]
    out=[]
    for k,f in enumerate(frames):
        face=['up','down','left','right'][(k%16)//4]
        # torso starts where the face ends: first row below the hair/face with orange (12)
        rows=[y for y in range(32) if 12 in f[y]]
        t=min(rows) if rows else 22
        g=[r[:] for r in f]
        for y in range(32):
            for x in range(32):
                v=f[y][x]
                if t<=y<t+4 and v==6 and not (face=='down' and abs(x-15.5)<=2): g[y][x]=12
                elif face=='down' and t<=y<t+4 and abs(x-15.5)<=2 and v in (12,10): g[y][x]=6
                elif y>=t and v==14: g[y][x]=6
                elif y>=t and v==7: g[y][x]=9
                elif y>=t+4 and v==3: g[y][x]=11
                elif y>=t+6 and v==10: g[y][x]=14
        out.append(g)
    P=list(pal); P[11]=(44,44,54); P[14]=(236,196,72)
    return out,P,im
if __name__=='__main__':
    out,P,im=convert()
    render(out,P,'/home/claude/ow/barry_new.png',S=4,grid=False)
    _,pal=load(SRC)
    render([frame(im,k) for k in (0,4,8,12)]+[out[k] for k in (0,4,8,12)],P[:0]+pal,'/home/claude/ow/barry_old.png',S=6,grid=False)
    render([out[k] for k in (0,4,8,12)],P,'/home/claude/ow/barry_big.png',S=8,grid=False)
