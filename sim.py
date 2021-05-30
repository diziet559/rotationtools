# sim.py

import rotationtools
import matplotlib.pyplot as plt

gearset = 'P1-BiS'

fight_length = 180

r = rotationtools.rotationplot('bm')
r.loadData('gear.yaml')
r.loadSet(gearset)
r.character.usingFlask = 1
r.character.gear.addWeapon(r.data, 'Sunfury', 'RangedWeapons')
print(r.melee.weapon.dps)
#r.character.gear.addWeapon(r.data, 'Legacy', 'Twohanders')
r.character.gear.changeTrinket1('Brooch')
r.character.gear.changeTrinket2('Slayers')

#r.character.gear.dst = 1
#r.character.talents.improvedAspectHawk = 5

t, dps, rhaste, mhaste, rotations, sps = r.mean_dps(fight_length, weaving=1, comp=1, use_drums = 1, haste_pot=1)

uniq = {x for l in rotations for x in l}

unfolded = [item for sublist in rotations for item in sublist]
rots_per_t = int(len(unfolded)/len(rotations))

hastes = []
    
for r2 in uniq:
    pos = unfolded.index(r2)
    xpos = int(pos/rots_per_t)
    ypos = pos % rots_per_t
    r3 = rotations[xpos][ypos]
    rh = rhaste[xpos]
    mh = round(mhaste[xpos], 2)
    if ypos>0:
        rh = rh*1.15
    rh = round(rh, 2)
    hastes.append((rh, mh))
    print(r2, xpos, ypos, r3)
    print(rh, mh)
    
rot_times = []
for r3 in uniq:
    rt = []
    start = -2
    stop = -2
    for i, rots in enumerate(rotations):
        if (start<0) and (r3 in rots):
            start = i
            print('started')
        if (start>=0) and not (r3 in rots):
            rt.append([start, i-1])
            start = -2
            print('ended')
        if (i==len(rotations)-1) and (r3 in rots):
            rt.append([start, i])
    rot_times.append(rt)

result = {}
result['rotations'] = list(uniq)
result['hastes'] = hastes

print('shots per second: {}'.format(sps))
ew = rotationtools.ew_uptime(1/sps, r.ranged.crit)
eew = ew * r.character.buffedAgi() / 4
print('Agi: {}, EW buff: {}, uptime: {}%, effective buff: {}'.format(int(r.character.buffedAgi()), int(r.character.buffedAgi()/4), round(ew*100), round(ew*int(r.character.buffedAgi()/4))))
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
print('Total: {dps:.0f} dps'.format(dps=sum(dps)/len(dps)))
ax.plot(t, dps)
ax.set_xlabel('time [s]')
ax.set_ylabel('dps')
ax.set_xlim([0, fight_length])
print(rot_times)
#ax.set_ylim([0, ax.get_ylim()[1]])
#ax.set_ylim([2000, 4000])
#ax2 = ax.twinx()
#ax2.plot(t, rhaste, 'r:')
#ax2.set_ylabel('haste')

print(r.mean_weights(180, weaving=1, comp=0, haste_pot=1, use_drums=1))
