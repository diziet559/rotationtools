import rotationtools
from itertools import product
#import matplotlib.pyplot as plt

if __name__ == "__main__":
    r = rotationtools.rotationplot()
    r.init_fig()
    h = 5
    m = 16
    prototype = 'as'
    r.melee_haste = (1+h/100)
    r.haste = 1.0 * 1.15 * r.melee_haste
    max_dps=0
    print('Searching optimum rotation for {}% haste, prototype {}, max. length {}'.format(h, prototype, m))
    for length in range(2,m+1-len(prototype)):
        print('Working on rotation length {} now.'.format(length+len(prototype)))
        for s in product('asmA', repeat=length):
            t = prototype + ''.join(s)
            if t.count('m')>1:
                continue
            if t.count('A')>1:
                continue
            if t.count('aaa')>1:
                continue
            if h>50 and t.count('ss')>1:
                continue
            r.clear()
            r.add_rotation(t)
            dps = r.calc_dps()
            if dps>max_dps:
                max_dps = dps
                current_best = t
                print(t, dps)
                r.init_fig()
                r.add_rotation(t)
                r.complete_fig()
    print('\nDone. Found optimum rotation {r} with {d:.0f} dps for a max. length of {l}.\nDISCLAIMER: Better but longer ones may exist.'.format(r=current_best,d=max_dps,l=m))