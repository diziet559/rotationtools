# sim.py

import rotationtools
import matplotlib.pyplot as plt


weaving_rotations = ['asmawsaswasAaws', 'asasw', 'asamwasasawsasasawAa', 'asawsasamawasasaAawasa', 'sawasaawasaa']
ranged_rotations = ['as', 'asa', 'asaa', 'asmasAasass', 'asmasasAasas', 'asAamasasasas', 'asasasaAaasasama', 'saasa', 'saaasaa']

weaving = 1
spec = 'bm'
gearset = 'd3t3'
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
    
    r = rotationtools.rotationplot(spec)
    r.character.gear.load(gearset)
    r.reloadChar()
    print(r.character.pet.dps())
    rotations = weaving_rotations if weaving else ranged_rotations
    haste_proc = 325 # dst 325
    haste_proc_uptime = 0.18 if r.character.gear.dst else 0
    for t in range(0,duration,1):
        time.append(t)
        haste = 1.0506 if use_drums else 1
        rapid_duration = 19 if r.character.gear.t3pc>=2 else 15
        if (t % 120)>=5 and (t % 120)<25:
            haste = haste + 0.2532 # haste pot is additive with drums
        haste_from_rating = haste
        if (t % 600)>=5 and (t % 600)<45:
            haste = haste * 1.3 # bloodlust
        ranged_haste = haste * 1.15 * (1.2 if spec=='bm' else 1)
        if (t % 180)>=5 and (t % 180)<(5 + rapid_duration):
            ranged_haste = ranged_haste * 1.5 # rapid fire
            
        if (len(mhaste_t)>0) and (haste==mhaste_t[-1]) and (ranged_haste==rhaste_t[-1]):
            dps = dps_t[-1] # don't need to recalc, nothing changed
        else:
            ihawk_time = hawk_uptime(3.0 / ranged_haste)
            if spec=='sv':
                ihawk_time = 0
            
            mhastes = [haste]
            rhastes = [ranged_haste]
            uptimes = []
            
            if haste_proc_uptime!=0:
                factor = (haste_from_rating + haste_proc/15.8/100) /haste_from_rating
                for n in range(0, len(mhastes)):
                    mhastes.append(mhastes[n] * factor) 
                    rhastes.append(rhastes[n] * factor)
            if ihawk_time>0:
                for n in range(0, len(mhastes)):
                    mhastes.append(mhastes[n])
                    rhastes.append(rhastes[n] * 1.15)
            
            if len(mhastes)==1:
                uptimes = [1]
            elif not haste_proc_uptime:
                uptimes = [1-ihawk_time, ihawk_time]
            elif not ihawk_time:
                uptimes = [1-haste_proc_uptime, haste_proc_uptime]
            else:
                uptimes = [0, haste_proc_uptime, ihawk_time, haste_proc_uptime*ihawk_time*1.1] # higher simultaneous uptime of both effects
                uptimes[0] = 1 - sum(uptimes[1:]) # calculate base eWS time
                
            dps_table = []
            
            if (t % 120)>=5 and (t % 120)<25:
                r.character.gear.total_rap = r.character.gear.total_rap + 278
                r.character.gear.total_map = r.character.gear.total_map + 278
                r.change_stats()
                
            for n in range(0, len(rhastes)):
                
                # find best rotation in loop
                
                dps = 0
                
                for rot in rotations:
                    r.clear()
                    r.melee.haste = mhastes[n]
                    r.ranged.haste = rhastes[n]
                    r.change_haste()
                    r.add_rotation(rot)
                    if (t % 120)>=5 and (t % 120)<23 and spec=='bm':
                        dps_new = r.calc_dps(r.calc_dur(),1.5/1.1) * 1.1
                    else:
                        dps_new = r.calc_dps(r.calc_dur(),1)
                    if dps_new>dps:
                        dps = dps_new
                
                dps_table.append(dps)
                
                # end rotation loop
            
            if (t % 120)>=5 and (t % 120)<25:
                r.character.gear.total_rap = r.character.gear.total_rap - 278
                r.character.gear.total_map = r.character.gear.total_map - 278
                r.change_stats()
        
        weighted_dps = [dps_table[n] * uptimes[n] for n in range(0,len(dps_table))]
        
        mhaste_t.append(haste)
        rhaste_t.append(ranged_haste)
        dps_t.append(sum(weighted_dps))
        
    return time, dps_t, rhaste_t

if __name__ == "__main__":
    t, dps, rhaste = mean_dps(fight_length)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    print(sum(dps)/len(dps))
    ax.plot(t, dps)
    ax.set_xlabel('time [s]')
    ax.set_ylabel('dps')
    ax2 = ax.twinx()
    ax2.plot(t, rhaste, 'r:')
    