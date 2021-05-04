# sim.py

import rotationtools
import matplotlib.pyplot as plt

gearset = 'D3T3'

fight_length = 180

r = rotationtools.rotationplot()
r.loadData('gear.yaml')
r.loadSet(gearset)
#r.character.gear.addWeapon(r.data, 'Wolfslayer', 'RangedWeapons')
#r.character.gear.addWeapon(r.data, 'QuantumBlade', 'Twohanders')

t, dps, rhaste = r.mean_dps(fight_length, weaving=1, use_drums = 1)
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
print('Total: {dps:.0f} dps'.format(dps=sum(dps)/len(dps)))
ax.plot(t, dps)
ax.set_xlabel('time [s]')
ax.set_ylabel('dps')
ax.set_xlim([0, fight_length])
#ax.set_ylim([0, ax.get_ylim()[1]])
ax.set_ylim([2000, 4000])
#ax2 = ax.twinx()
#ax2.plot(t, rhaste, 'r:')
#ax2.set_ylabel('haste')
