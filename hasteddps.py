import rotationtools
import matplotlib.pyplot as plt

if __name__ == "__main__":
    spec_dps = []
    for spec in ['bm', 'sv']:
        names = ['as', 'aas', 'aaas', 'asmasAasass', 'asmasasAasas', 'asAamasasasas', 'asasasaAaasasama']
        #spec = 'sv'
        plotit = 0
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
            for h in range(200,351,1):
                x.append(h)
                rot.melee_haste = (1+h/100)
                rot.ranged.haste = (1.2 if spec=='bm' else 1) * 1.15 * (1+h/100)
                rot.change_haste()
                #rot.set_sv()
                #rot.haste = 1.2 * 1.15 * rot.melee_haste
                rot.recalc()
                dps.append(rot.calc_dps(rot.calc_dur()))
            d.append(dps)
        if plotit==1:
            plt.subplots(figsize=(10, 6), dpi=150)
            for dps in d:
                plt.plot(x, dps)
                #plt.plot((15, 15),(1000,2000),'k:')
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
        spec_dps.append(max_dps)
    
    if plotit==2:
        ax = plt.subplots(figsize=(10, 6), dpi=150)
        for dps in spec_dps:
            plt.plot(x, dps)
        #plt.plot((15, 15),(1000,2000),'k:')
        #plt.plot((237, 237), (1600,2300))
        plt.xlabel('additional haste [%]')
        plt.ylabel('dps')
        plt.legend(['BM', 'Surv'])
    
    spec_dps.append(spec_dps[0])
    spec_dps.append(spec_dps[1])
    
    spec_dps_t = []
    spec_dps_mean = []
    for n, dps in enumerate(spec_dps):
        dps_t = []
        time = []
        haste_t = []
        for t in range(0,180,1):
            time.append(t)
            haste = 1.05
            if (t % 600)>=5 and (t % 600)<45:
                haste = haste * 1.3 # bloodlust
            if (t % 180)>=5 and (t % 180)<20:
                haste = haste * 1.4 # rapid fire
            if (t % 120)>=5 and (t % 120)<25:
                haste = haste * 1.25 # haste pot
            
            if n>=2:
                haste = haste * 1.15 # sim 100% hawk uptime
            
            haste_t.append(round((haste-1)*100))
            current_dps = dps[haste_t[-1]]
            if (t % 120)>=5 and (t % 120)<25:
                current_dps = current_dps + 0.51 * 278
                if n==0:
                    current_dps = current_dps * 1.1 # the beast within
            dps_t.append(current_dps)
            
        spec_dps_t.append(dps_t)
        spec_dps_mean.append(round(sum(dps_t)/len(dps_t)))
        
    ax = plt.subplots(figsize=(10, 6), dpi=150)
    plt.fill_between(time, spec_dps_t[0], spec_dps_t[2], alpha=0.6, linestyle='-', color='chocolate')
    plt.fill_between(time, spec_dps_t[1], spec_dps_t[3], alpha=0.6, linestyle='-', color='limegreen')
    #plt.plot(time, spec_dps_t[0], spec_dps_t[0], color='chocolate')
    #plt.plot(time, spec_dps_t[0], spec_dps_t[2], color='chocolate')
    #plt.plot(time, spec_dps_t[0], spec_dps_t[1], color='limegreen')
    #plt.plot(time, spec_dps_t[0], spec_dps_t[3], color='limegreen')
    plt.xlabel('time [s]')
    plt.ylabel('dps')
    plt.legend(['BM (avg. {dpsmin:.0f} - {dpsmax:.0f})'.format(dpsmin=spec_dps_mean[0],dpsmax=spec_dps_mean[2]), \
                'Surv (avg. {dpsmin:.0f} - {dpsmax:.0f})'.format(dpsmin=spec_dps_mean[1],dpsmax=spec_dps_mean[3])])
    