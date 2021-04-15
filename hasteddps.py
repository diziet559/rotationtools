import rotationtools
import abilities
import matplotlib.pyplot as plt

if __name__ == "__main__":
    names = ['as', 'ass', 'asmasAasass', 'asmasasAasas', 'asAamasasasas', 'asmasasaAasas', 'asasasaAaasasama']
    labels = []
    rotations = []
    for n in names:
        r = rotationtools.rotationplot()
        r.add_rotation(n)
        rotations.append(r)
        labels.append(rotationtools.shorthand(n))
    d = []
    for rot in rotations:
        x = []
        dps = []
        for h in range(0,101,1):
            x.append(h)
            rot.melee_haste = (1+h/100)
            rot.ranged.haste = 1.2 * 1.15 * (1+h/100)
            rot.abilities = abilities.create(rot.ranged, rot.melee)
            #rot.set_sv()
            #rot.haste = 1.2 * 1.15 * rot.melee_haste
            rot.recalc()
            dps.append(rot.calc_dps(rot.calc_dur()))
        d.append(dps)
    ax = plt.subplots(figsize=(10, 6), dpi=150)
    for dps in d:
        plt.plot(x, dps)
    #plt.plot((237, 237), (1600,2300))
    plt.xlabel('additional haste [%]')
    plt.ylabel('dps')
    plt.legend(labels)
    
    max_dps = []
    for count, value in enumerate(x):
        rot_dps = []
        for dps in d:
            rot_dps.append(dps[count])
        max_dps.append(max(rot_dps))
        
    