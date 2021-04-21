import rotationtools
import matplotlib.pyplot as plt

if __name__ == "__main__":
    names = ['as', 'asa', 'asaa', 'asmasAasass', 'asmasasAasas', 'asAamasasasas', 'asasasaAaasasama', 'asaas', 'aasaaas']
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
        for h in range(-99,251,1):
            x.append(h)
            rot.melee_haste = (1+h/100)
            rot.ranged.haste = (1.2 if spec=='bm' else 1) * 1.15 * (1+h/100)
            rot.change_haste()
            #rot.set_sv()
            #rot.haste = 1.2 * 1.15 * rot.melee_haste
            rot.recalc()
            dps.append(rot.calc_dps(rot.calc_dur()))
        d.append(dps)
    plt.subplots(figsize=(10, 6), dpi=150)
    for dps in d:
        plt.plot(x, dps)
        #plt.plot((15, 15),(1000,2000),'k:')
        #plt.plot((237, 237), (1600,2300))
        plt.xlabel('additional haste [%]')
        plt.ylabel('dps')
        plt.legend(labels)