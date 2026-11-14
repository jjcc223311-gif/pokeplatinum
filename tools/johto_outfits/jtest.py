import sys;sys.path.insert(0,'/home/claude/ow')
from common import *
import importlib, jun_tmpl as T
def place(f,tm,dy=0,dx=0):
    n=[r[:] for r in f]
    for y,pieces in tm.items():
        for x,s in pieces:
            for i,c in enumerate(s):
                X,Y=x+i+dx,y+dy
                if 0<=X<32 and 0<=Y<32 and c!=' ': n[Y][X]=0 if c=='.' else CH.index(c)
    return n
if __name__=='__main__':
    im,pal=load('/home/claude/pokeplatinum/res/graphics/field_sprites/player/player_f.png')
    out=[]
    for k,key in [(int(a.split(':')[0]),a.split(':')[1]) for a in sys.argv[2:]]:
        f=frame(im,k);out+=[f,place(f,getattr(T,key))]
    render(out,pal,sys.argv[1],S=7)
