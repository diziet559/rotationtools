# sim.py

import rotationtools
import matplotlib.pyplot as plt


weaving_rotations = ['asmawsaswasAaws', 'asasw', 'asamwasasawsasasawAa', 'asawsasamawasasaAawasa', 'sawasaawasaa']
ranged_rotations = ['as', 'asa', 'asaa', 'asmasAasass', 'asmasasAasas', 'asAamasasasas', 'asasasaAaasasama', 'saasa', 'saaasaa']

weaving = 0
spec = 'bm'
gearset = 'bm-primal'
fight_length = 180

def hawk_uptime(ews):
    proc_chance = 0.1
    haste = 1.15
    duration = 12
    
    attacks_during = int(duration/ews*haste)
    
    drop_chance = 0.9**attacks_during
    cont_dur = sum([0.9**n * 0.1 * ews/1.15 * (n+1) for n in range(0,attacks_during)])
    
    mean_dur = 12 + cont_dur / (1-drop_chance)
    mean_pause = ews / proc_chance
    
    return mean_dur / (mean_dur + mean_pause)

def mean_dps(duration):
    use_drums = 1
    dps_t = []
    time = []
    mhaste_t = []
    rhaste_t = []
    
    #haste_proc = 400 # dst 400
    #haste_proc_uptime = 10 / 60 # 1 ppm, 10 sec duration
    r = rotationtools.rotationplot(spec)
    r.character.gear.load(gearset)
    r.reloadChar()
    print(r.character.pet.buffedStats())
    print(r.character.pet.dps())
    rotations = weaving_rotations if weaving else ranged_rotations
    for t in range(0,duration,1):
        time.append(t)
        haste = 1.05 if use_drums else 1
        rapid_duration = 19 if r.character.gear.t3pc>=2 else 15
        if (t % 120)>=5 and (t % 120)<25:
            haste = haste + 0.25 # haste pot is additive with drums
        #if haste_proc > 0:
        #    haste_procced = haste + haste_proc/1600 # haste rating is additive
        #else:
        #    haste_procced = None
        if (t % 600)>=5 and (t % 600)<45:
            haste = haste * 1.3 # bloodlust
        ranged_haste = haste * 1.15 * (1.2 if spec=='bm' else 1)
        if (t % 180)>=5 and (t % 180)<(5 + rapid_duration):
            ranged_haste = ranged_haste * 1.5 # rapid fire
            
        if (len(mhaste_t)>0) and (haste==mhaste_t[-1]) and (ranged_haste==rhaste_t[-1]):
            dps = dps_t[-1] # don't need to recalc, nothing changed
        else:
            ihawk_haste = ranged_haste * 1.15
            ihawk_time = hawk_uptime(3.0 / ranged_haste)
            if spec=='sv':
                ihawk_time = 0
            
            dps = 0
            if (t % 120)>=5 and (t % 120)<25:
                r.character.gear.total_rap = r.character.gear.total_rap + 278
                r.character.gear.total_map = r.character.gear.total_map + 278
                r.change_stats()
            for rot in rotations:
                r.clear()
                r.melee.haste = haste
                r.ranged.haste = ranged_haste
                r.change_haste()
                r.add_rotation(rot)
                if (t % 120)>=5 and (t % 120)<23 and spec=='bm':
                    dps_new = r.calc_dps(r.calc_dur(),1.5/1.1)
                else:
                    dps_new = r.calc_dps(r.calc_dur(),1)
                r.ranged.haste = ihawk_haste
                r.change_haste()
                r.recalc()
                if (t % 120)>=5 and (t % 120)<23 and spec=='bm':
                    dps_hawk = r.calc_dps(r.calc_dur(),1.5/1.1)
                else:
                    dps_hawk = r.calc_dps(r.calc_dur(),1)
                dps_mean = ihawk_time * dps_hawk + (1-ihawk_time) * dps_new
                if dps_new>dps:
                    dps = dps_mean
            if (t % 120)>=5 and (t % 120)<25:
                r.character.gear.total_rap = r.character.gear.total_rap - 278
                r.character.gear.total_map = r.character.gear.total_map - 278
                r.change_stats()
            if (t % 120)>=5 and (t % 120)<25 and spec=='bm':
                dps = dps * 1.1 # the beast within

        mhaste_t.append(haste)
        rhaste_t.append(ranged_haste)
        dps_t.append(dps)
        
    return time, dps_t

if __name__ == "__main__":
    t, dps = mean_dps(fight_length)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    print(sum(dps)/len(dps))
    ax.plot(t, dps)
    ax.set_xlabel('time [s]')
    ax.set_ylabel('dps')
    