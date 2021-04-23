import rotationtools
import matplotlib.pyplot as plt
import numpy as np

def separate_haste(total_haste, spec='bm'):
    if spec=='bm':
        total_haste = total_haste / 1.2 # bm talent haste will be added back later
    if total_haste <= 1.15:
        melee_haste = total_haste / 1.15 # always assume quiver
    elif total_haste > 1.15 * 1.15 * 1.5: # max range haste: RF+quiver+hawk
        melee_haste = total_haste / (1.15 * 1.15 * 1.5)
    else:
        melee_haste = 1   
    if spec=='bm':
        total_haste = total_haste * 1.2 # add bm talent haste back
    return total_haste, melee_haste

if __name__ == "__main__":
    spec = 'bm'
    weaving = 1
    if weaving:
        names = ['asmawsaswasAaws', 'asasw', 'asamwasasawsasasawAa', 'asawsasamawasasaAawasa', 'sawasaawasaa', 'as', 'asa', 'asaa'] # 'asawsasamawsasasawA' optimal at 30% ranged-only haste
    else:
        names = ['as', 'asa', 'asaa', 'asmasAasass', 'asmasasAasas', 'asAamasasasas', 'asasasaAaasasama', 'saasa', 'saaasaa']
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
            total_haste = h/100 * 1.15
            if spec=='bm':
                total_haste = total_haste * 1.2
            rhaste, mhaste = separate_haste(total_haste, spec)
            rot.melee.haste = mhaste
            rot.ranged.haste = rhaste
            rot.change_haste()
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
    for n, dps in enumerate(d):
        if weaving and labels[n].find('w')<0:
            ax.plot(x, dps, ':')
        else:
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
    