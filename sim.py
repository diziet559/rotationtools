# sim.py

import rotationtools
import matplotlib.pyplot as plt

gearset = 'P1-BiS'

fight_length = 180

r = rotationtools.rotationplot('bm')
r.loadData('gear.yaml')
r.loadSet(gearset)

t, dps, rhaste = r.mean_dps(fight_length)
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
print('Total: {dps:.0f} dps'.format(dps=sum(dps)/len(dps)))
ax.plot(t, dps)
ax.set_xlabel('time [s]')
ax.set_ylabel('dps')
ax2 = ax.twinx()
ax2.plot(t, rhaste, 'r:')
ax2.set_ylabel('haste')
