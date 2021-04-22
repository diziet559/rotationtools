import rotationtools
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    names = ['as', 'asa', 'asaa', 'asmasAasass', 'asmasasAasas', 'asAamasasasas', 'asasasaAaasasama', 'saasa', 'saaasaa']
    spec = 'bm'
    labels = []
    rotations = []
    for n in names:
        r = rotationtools.rotationplot(spec)
        
        r.add_rotation(n)
        rotations.append(r)
        labels.append(rotationtools.shorthand(n))
    d = []
    for rot in rotations:
        x = []
        dps = []
        for h in range(100,351,1):
            x.append(h/100)
            rot.melee_haste = h/100#(1+h/100)
            rot.ranged.haste = (1.2 if spec=='bm' else 1) * 1.15 * rot.melee_haste
            rot.change_haste()
            #rot.set_sv()
            #rot.haste = 1.2 * 1.15 * rot.melee_haste
            rot.recalc()
            dps.append(rot.calc_dps(rot.calc_dur()))
        d.append(dps)
    def tick_func(x):
        static_haste = (1.2 if spec=='bm' else 1) * 1.15
        V = 2.9 / static_haste / x
        return ["%.2f" % z for z in V]
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.grid(True)
    ax2 = ax.twiny()
    for dps in d:
        ax.plot(x, dps)
        #plt.plot((15, 15),(1000,2000),'k:')
        #plt.plot((237, 237), (1600,2300))
    #top_tick_locs = np.array([2.9/2.0, 2.9/1.5, 2.9/1.2, 2.9/1.0, 2.9/0.9])
    top_tick_locs = np.array([1, 1.15, 1.3, 1.5, 1.15*1.5, 1.3*1.5, 1.15*1.3*1.5, 1.3*1.5*1.3, 1.15*1.3*1.5*1.3, 1.15*1.3*1.5*1.5])
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(top_tick_locs)
    ax2.set_xticklabels(tick_func(top_tick_locs))
    ax2.set_xlabel('effective weapon swing')
    
    ax.set_yticks([])
    ax.set_xticks([1, 1.15, 1.3, 1.5, 1.15*1.5, 1.3*1.5, 1.15*1.3*1.5, 1.3*1.5*1.3, 1.15*1.3*1.5*1.3, 1.15*1.3*1.5*1.5])
    ax.set_xticklabels(['reg', 'hawk', 'lust', 'RF or\nhawk, lust', 'RF, hawk', 'RF, lust', 'RF, hawk, lust', 'RF,\nlust, pot', 'RF, (hawk or DST),\nlust, pot', 'RF, hawk, lust,\npot, DST'])
    #ax.set_xlabel('total haste')
    ax.set_ylabel('dps')
    ax.legend(labels)
    