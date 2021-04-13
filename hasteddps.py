import rotationtools
import matplotlib.pyplot as plt

if __name__ == "__main__":
    names = ['as', 'ass', 'aas', 'aaas', 'asmasasAasas', 'asasasaAaasasama']
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
        for h in range(-20,301,1):
            x.append(h)
            rot.haste = 1.15 * (1+h/100)
            rot.melee_haste = (1+h/100)
            rot.recalc()
            dps.append(rot.calc_dps())
        #r.add_rotation('asmarsasAawsasaws') # 6:6:1:1:1:1 french 3-weave
        d.append(dps)
    ax = plt.subplots(figsize=(10, 6), dpi=150)
    for dps in d:
        plt.plot(x, dps)
    #plt.plot((237, 237), (1600,2300))
    plt.xlabel('additional haste [%]')
    plt.ylabel('dps')
    plt.legend(labels)
    