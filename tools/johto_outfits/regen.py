import sys;sys.path.insert(0,'/home/claude/ow')
import lucas_rgb as L, jun_rgb as J
OUT='/home/claude/pokeplatinum/res/johto_outfits/field_sprites/'
names=['','_bike','_fishing','_holding_pokeball','_pokecenter_heal','_poketch','_save','_sprayduck','_surf','_vs_seeker']
which=sys.argv[1]
for n in names:
    M=L if which=='m' else J
    fr,bg,info=M.convert(M.SRC+f'player_{which}{n}.png'); L.save(fr,bg,OUT+f'player/player_{which}{n}.png')
    L.preview(fr,f'/home/claude/ow/rev_{which}{n}.png',S=5,per=12,labels=[str(i) for i in range(len(fr))])
