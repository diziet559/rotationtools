#!/usr/bin/env python3
import matplotlib.pyplot as plt
import damage
import abilities
import talents
import yaml
from math import ceil

def hawk_uptime(ews):
    proc_chance = 0.1
    haste = 1.15
    duration = 12

    attacks_during = int(duration/ews*haste)

    drop_chance = 0.9**attacks_during
    cont_dur = sum([0.9**n * 0.1 * ews/haste * (n+1) for n in range(0,attacks_during)])

    mean_dur = duration + cont_dur / (1-drop_chance)
    mean_pause = ews / proc_chance - ews/2

    return mean_dur / (mean_dur + mean_pause)

def ew_uptime(ews, crit):
    proc_chance = crit/100
    duration = 7

    attacks_during = int(duration/ews)

    drop_chance = (1-crit)**attacks_during
    cont_dur = sum([(1-crit)**n * crit * ews * (n+1) for n in range(0,attacks_during)])

    mean_dur = duration + cont_dur / (1-drop_chance)
    mean_pause = ews / proc_chance - ews/2

    return mean_dur / (mean_dur + mean_pause)

def shorthand(s):
    autos = s.count('a')
    steadies = s.count('s')
    multis = s.count('m')
    arcanes = s.count('A')
    weaves = s.count('w')
    raptors = s.count('r')
    out = str(steadies) + ':' + str(autos)
    if (multis>0) or (arcanes>0):
        out = out + ':' + str(multis) + ':' + str(arcanes)
    if (weaves>0) or (raptors>0):
        out = out + ' ' + str(weaves+raptors) + 'w'
    return out


class rotationplot:
    character = talents.Character('')

    rotation_string = ''

    current_time = 0
    total_damage = 0
    remaining_armor = 6200 - 3075 - 610 - 800 # base - iEA - FF - CoR

    hawk_until = -1

    ax = None
    showlabels = 1 # set to true to show labels on all shotss
    rot_stats = 'Ranged speed: {speed:.1f}\nRanged haste: {haste:.2f}\nDuration: {dur:.2f}'
    dps_stats = 'AP: {rap:.0f} (r)/ {map:.0f} (m)\nCrit: {crit:.1f}%\nDPS: {dps:.0f} / Pet: {petdps:.0f}\nTotal: {totaldps:.0f}'
    row0 = {
        'Auto': 0.1,
        'Cast': 1.1,
        'GCD': 2.1,
    }

    def __init__(self, s=None):
        if not s:
            s = 'bm'
        self.character = talents.Character(s)
        avgRngDmg = self.character.buffedStats(1)
        self.ranged = damage.AverageRangedDamage(avgRngDmg[0],avgRngDmg[1],avgRngDmg[2],avgRngDmg[3],avgRngDmg[4],avgRngDmg[5])
        avgMeleeDmg = self.character.buffedStats(0)
        self.melee = damage.AverageMeleeDamage(avgMeleeDmg[0],avgMeleeDmg[1],avgMeleeDmg[2],avgMeleeDmg[3],avgMeleeDmg[4])
        self.abilities = abilities.create(self.ranged, self.melee)
        self.abilities['multi'].damage = self.abilities['multi'].damage * (1 + self.character.talents.barrage * 0.04)

    def reloadChar(self):
        avgRngDmg = self.character.buffedStats(1)
        self.ranged = damage.AverageRangedDamage(avgRngDmg[0],avgRngDmg[1],avgRngDmg[2],avgRngDmg[3],avgRngDmg[4],avgRngDmg[5])
        avgMeleeDmg = self.character.buffedStats(0)
        self.melee = damage.AverageMeleeDamage(avgMeleeDmg[0],avgMeleeDmg[1],avgMeleeDmg[2],avgMeleeDmg[3],avgMeleeDmg[4])
        self.abilities = abilities.create(self.ranged, self.melee)
        self.abilities['multi'].damage = self.abilities['multi'].damage * (1 + self.character.talents.barrage * 0.04)

    def init_fig(self):
        self.clear()
        fig, self.ax = plt.subplots(figsize=(10, 6), dpi=150)

    def clear(self):
        self.rotation_string = ''
        self.current_time = 0
        self.total_damage = 0

        for ability in self.abilities.values():
            ability.reset()

        self.ax = None

    def setTalents(self, s):
        self.talents.load(s)

    def recalc(self):
        s = self.rotation_string
        self.clear()
        self.add_rotation(s)

    def change_haste(self):
        self.abilities['auto'].duration = 0.5 / self.ranged.haste
        self.abilities['auto'].cd = (self.ranged.weapon.speed - 0.5) / self.ranged.haste
        self.abilities['steady'].duration = 1.5 / self.ranged.haste
        self.abilities['multi'].duration = 0.5 / self.ranged.haste
        self.abilities['melee'].cd = self.melee.weapon.speed / self.melee.haste - self.abilities['melee'].duration

    def change_stats(self):
        avgRngDmg = self.character.buffedStats(1)
        self.ranged = damage.AverageRangedDamage(avgRngDmg[0],avgRngDmg[1],avgRngDmg[2],avgRngDmg[3],avgRngDmg[4],avgRngDmg[5], t5pc=self.character.gear.t5pc, t6pc=self.character.gear.t6pc)
        avgMeleeDmg = self.character.buffedStats(0)
        self.melee = damage.AverageMeleeDamage(avgMeleeDmg[0],avgMeleeDmg[1],avgMeleeDmg[2],avgMeleeDmg[3],avgMeleeDmg[4])
        self.abilities = abilities.create(self.ranged, self.melee)
        self.abilities['multi'].damage = self.abilities['multi'].damage * (1 + self.character.talents.barrage * 0.04)

    def calc_dur(self, verbose=0):
        if verbose:
            print(self.current_time)
            print([
                ability
                for ability in abilities.ABILITIES_WITH_CD
            ])
            print([
                self.abilities[ability].available
                for ability in abilities.ABILITIES_WITH_CD
            ])
            print([
                self.abilities[ability].first_usage
                for ability in abilities.ABILITIES_WITH_CD
            ])
            print([
                max(self.abilities[ability].available, self.current_time) - self.abilities[ability].first_usage
                for ability in abilities.ABILITIES_WITH_CD
            ])
        if self.abilities['gcd'].first_usage<0:
            self.abilities['gcd'].first_usage = self.abilities['gcd'].first_usage + 1.5 # first usage seems weird for gcd
        return max([
            max(self.abilities[ability].available, self.current_time) - self.abilities[ability].first_usage
            for ability in abilities.ABILITIES_WITH_CD
        ])

    def calc_dps(self, duration, pet = 0):
        pet_dps = self.character.pet.dps()
        self.remaining_armor = 6200 - self.character.raid.debuffs()[-1]
        armor = max(0, self.remaining_armor - self.character.gear.arpen)
        return (pet * pet_dps + self.total_damage / duration) * (1 - (armor / ((467.5 * 70) + armor - 22167.5)))

    def statweights(self, pet_mod=1):
        self.change_stats()
        self.recalc()
        base_dps = self.calc_dps(self.calc_dur(), pet_mod)

        # increase ap by 1 for ap weight
        self.character.gear.total_rap = self.character.gear.total_rap + 1
        self.character.gear.total_map = self.character.gear.total_map + 1
        self.change_stats()
        self.recalc()
        ap_dps = self.calc_dps(self.calc_dur(), pet_mod)

        # also increase agi for agi weight, total ap includes agi already
        self.character.gear.agi = self.character.gear.agi + 1
        self.change_stats()
        self.recalc()
        agi_dps = self.calc_dps(self.calc_dur(), pet_mod)

        # undo ap and agi changes
        self.character.gear.total_rap = self.character.gear.total_rap - 1
        self.character.gear.total_map = self.character.gear.total_map - 1
        self.character.gear.agi = self.character.gear.agi - 1
        # increase crit rating by 1 for crit weight
        self.character.gear.crit_rating = self.character.gear.crit_rating + 1
        self.change_stats()
        self.recalc()
        crit_dps = self.calc_dps(self.calc_dur(), pet_mod)

        # undo crit rating
        self.character.gear.crit_rating = self.character.gear.crit_rating - 1
        self.change_stats()
        # increase haste for haste rating weight
        self.melee.haste = self.melee.haste * (1+1/15.8/100)
        self.ranged.haste = self.ranged.haste * (1+1/15.8/100)
        self.change_haste()
        self.recalc()
        haste_dps = self.calc_dps(self.calc_dur(), pet_mod)

        # calculate stat weights from dps values for each stat
        ap_weight = ap_dps - base_dps
        agi_weight = (agi_dps - base_dps)
        crit_weight = (crit_dps - base_dps)
        haste_weight = (haste_dps - base_dps)

        # return to old values
        self.melee.haste = self.melee.haste / (1+1/15.8/100)
        self.ranged.haste = self.ranged.haste / (1+1/15.8/100)
        self.change_haste()
        self.recalc()

        return base_dps, ap_weight, agi_weight, crit_weight, haste_weight


    def complete_fig(self, title=None, legend = 1):
        #self.ax.set_xlim(-0.25, 12)
        self.ax.set_ylim(0, 3)
        self.ax.set_yticks([0.5, 1.5, 2.5])
        self.ax.set_yticklabels(self.row0.keys())
        self.ax.set_xlabel('time [s]')
        labels = list(self.abilities.keys())
        handles = [plt.Rectangle((0,0),1,1, color=self.abilities[label].color) for label in labels]
        if legend:
            plt.legend(handles, labels, bbox_to_anchor=(1.005, 1), loc='upper left')
        duration = self.calc_dur()
        dps = self.calc_dps(duration)
        petdps = 1.0 * self.character.pet.dps() * (1 - (self.remaining_armor / ((467.5 * 70) + self.remaining_armor - 22167.5)))
        totaldps = dps + petdps
        rota = self.rot_stats.format(speed = self.ranged.speed(), haste = self.ranged.haste, dur=duration)
        if legend:
            plt.annotate(rota,(1.005,0.5), xycoords='axes fraction')
        stats = self.dps_stats.format(rap=self.ranged.ap,map=self.melee.ap,crit=self.ranged.crit,dps=dps,petdps=petdps,totaldps=totaldps)
        if legend:
            plt.annotate(stats,(1.005,0.35), xycoords='axes fraction')
        gcd_eff = self.abilities['gcd'].count * 1.5 / duration
        auto_eff = self.abilities['auto'].count * (self.abilities['auto'].duration + self.abilities['auto'].cd) / duration
        eff_str = 'gcd efficiency: ' + str(round(gcd_eff*100)) + '%\nauto efficiency: ' + str(round(auto_eff*100)) + '%'
        if self.abilities['melee'].count>0 or self.abilities['raptor'].count>0:
            weave_count = self.abilities['raptor'].count + self.abilities['melee'].count
            eff_str = eff_str + '\nweaving efficiency: ' + str(round(weave_count * (self.abilities['melee'].cd+self.abilities['melee'].duration) / duration * 100)) + '%'
        if legend:
            plt.annotate(
                eff_str,
                (1.005, 0.23), xycoords='axes fraction'
            )
            plt.annotate(
                abilities.create_breakdown(self.abilities, self.total_damage),
                (1.005, -0.03), xycoords='axes fraction'
            )
        self.ax.set_xlim(0, duration)
        if title:
            plt.title(title)
        #plt.annotate('Range haste: '+str(self.haste),(1.01,0.455), xycoords='axes fraction')
        plt.show()

    def add_ability(self, ability_name, y1, update_time = True):
        ability = self.abilities[ability_name]

        if ability.has_availability and ability.available > self.current_time:
            self.current_time = ability.available

        self.add_concrete_ability(ability, y1, None, update_time)

    def add_concrete_ability(self, ability, y1, x0 = None, update_time = True):
        if (x0 is None):
            x0 = self.current_time

        if self.ax:
            self.ax.bar(
                x0, ability.height, ability.duration, y1,
                facecolor = 'white',
                edgecolor = ability.color,
                align = 'edge'
            )

        if self.ax and self.showlabels and ability.has_annotation:
            plt.annotate(
                ability.annotation, (self.current_time + ability.duration / 2, y1 + 0.4),
                ha='center', va='center'
            )
        
        self.total_damage = self.total_damage + ability.damage
        

        if (update_time):
            self.current_time = self.current_time + ability.duration

        ability.use(self.current_time)

    def add_auto_delay(self):
        auto = self.abilities['auto']
        delay = self.current_time - auto.available

        if (delay <= 0):
            return

        self.add_concrete_ability(
            abilities.auto_delay(delay),
            0.4, auto.available, False
        )
        if self.ax:
            plt.annotate(
                '{delay:.2f}'.format(delay=delay), (self.current_time-0.02, 0.25),
                ha='right', va='center'
            )


    def add_auto(self):
        self.add_auto_delay()
        self.add_ability('auto', self.row0['Auto'])

    def add_gcd_ability(self, ability_name):
        self.add_ability('gcd', self.row0['GCD'], False)
        self.add_ability(ability_name, self.row0['Cast'])

    def add_raptor(self):
        self.add_ability('raptor', self.row0['Cast'])

    def add_melee(self):
        self.add_ability('melee', self.row0['Cast'])

    def add_rotation(self, s):
        self.rotation_string = s

        melee_dmg = self.abilities['melee'].damage
        raptor_dmg = self.abilities['raptor'].damage

        if self.character.raid.grp.enha==1:
            self.abilities['melee'].damage =self.abilities['melee'].damage + 0.2 * melee_dmg
            self.abilities['raptor'].damage =self.abilities['raptor'].damage + 0.2 * melee_dmg
        
        if s.count('r')==0 and s.count('w')>0:
            raptor_every = ceil(self.abilities['raptor'].cd/self.abilities['melee'].cd)
            mean_dmg = (self.abilities['melee'].damage * (raptor_every - 1) + self.abilities['raptor'].damage) / raptor_every
            self.abilities['melee'].damage = mean_dmg
        
        for c in s:
            if self.current_time>self.hawk_until and self.hawk_until>0:
                self.ranged.haste = self.ranged.haste / 1.15 # un-proc imp hawk
                self.change_haste()
                self.hawk_until = -1

            if c=='a':
                self.add_auto()
            elif c=='A':
                self.add_gcd_ability('arcane')
            elif c=='s':
                self.add_gcd_ability('steady')
            elif c=='m':
                self.add_gcd_ability('multi')
            elif c=='r':
                self.add_raptor()
            elif c=='w':
                self.add_melee() # white hit
            elif c=='h':
                if self.current_time>self.hawk_until:
                    self.ranged.haste = self.ranged.haste * 1.15 # manually proc imp hawk for testing
                    self.change_haste()
                self.hawk_until = self.current_time + 12
        
        self.abilities['melee'].damage = melee_dmg
        self.abilities['raptor'].damage = raptor_dmg

    def loadSet(self, name):
        self.character.gear.load(self.data, name)

    def loadData(self, f):
        with open('gear.yaml') as f:
            self.data = yaml.safe_load(f)

    def mean_dps(self, duration, weaving = 0, comp = 0, use_drums = 0, drum_timing = 5, haste_pot = 0, silent = 0):
        dps_t = []
        sps_t = []
        time = []
        mhaste_t = []
        rhaste_t = []
        rotations_t = []

        if not silent:
            print('Running simulation for set {} with {} / {}.'.format(self.character.gear.setname, self.character.gear.rweaponname, self.character.gear.mweaponname))
            optionstr = ('Complex' if comp else 'Simple') + ' rotations. '
            optionstr = optionstr + ('Melee' if weaving else 'No') + ' weaving.' + '\n'
            if use_drums==1:
                optionstr = optionstr + 'Haste drums after ' + str(drum_timing) + ' seconds.\n'
            elif use_drums==2:
                optionstr = optionstr + 'AP drums after ' + str(drum_timing) + ' seconds.\n'
            else:
                optionstr = optionstr + 'No drums.\n'
            optionstr = optionstr + ('Using haste pot with BW/TBW and trinket. ' if haste_pot else 'No haste pots.')
            print(optionstr)
            #self.reloadChar()
            #print('Pet does {petdps:.0f} dps.'.format(petdps=r.character.pet.dps()))
            print()
        rotations = self.data['Rotations']['Weaving'] if weaving else self.data['Rotations']['Ranged']
        print(len(rotations))
        if comp:
            rotations = rotations + self.data['Rotations']['ComplexWeaving'] if weaving else self.data['Rotations']['ComplexRanged']
        print(len(rotations))
        haste_proc = 325 # dst 325
        haste_proc_uptime = 0.27 if self.character.gear.dst else 0
        self.change_stats()
        rapid_duration = 19 if self.character.gear.t3pc>=2 else 15
        recalc_on = []
        for t in range(0,duration,1):
            addthis = 0
            if t==0:
                addthis = 1
            elif (t % 120) in [5, 20, 23, 25, drum_timing, drum_timing+30, 5+self.character.gear.use1dur, 5+self.character.gear.use1dur+self.character.gear.use2dur]:
                addthis = 1
            elif (t % 180) in [5, 5+rapid_duration]:
                addthis = 1
            elif (t % 600) in [5, 45]:
                addthis = 1
            elif self.character.talents.masterTactician>0 and t<8:
                # to get MT procs up
                addthis = 1
            if addthis:
                recalc_on.append(t)
        
        for t in range(0,duration,1):
            time.append(t)
    
            if not t in recalc_on:
                mhaste_t.append(mhaste_t[-1])
                rhaste_t.append(rhaste_t[-1])
                dps_t.append(dps_t[-1])
                sps_t.append(sps_t[-1])
                rotations_t.append(rotations_t[-1])
                continue
            
            mt_crit = 0
            if self.character.talents.masterTactician and t>0:
                if t<8:
                    mtShots = sum(sps_t)
                else:
                    mtShots = sum(sps_t[-8:])
                mt_crit = 2 * self.character.talents.masterTactician * (1 - (1 - 0.06)**(int(mtShots)))

            self.character.gear.crit_rating += mt_crit*22.1
            
            haste = 1 + self.character.gear.haste_rating / 1577
            if (t % 120)>=drum_timing and (t % 120)<(drum_timing+30) and use_drums==1:
                haste = haste + 0.0506
            if (t % 120)>=drum_timing and (t % 120)<(drum_timing+30) and use_drums==2:
                self.character.usingDrums = use_drums
            else:
                self.character.usingDrums = 0
            if (t % 120)>=5 and (t % 120)<20 and haste_pot:
                haste = haste + 0.2532 # haste pot is additive with drums
            haste_from_rating = haste
            if (t % 600)>=5 and (t % 600)<45:
                haste = haste * 1.3 # bloodlust
            ranged_haste = haste * 1.15 * (1 + 0.04 * self.character.talents.serpentsSwiftness)
            if (t % 180)>=5 and (t % 180)<(5 + rapid_duration):
                ranged_haste = ranged_haste * 1.4 # rapid fire

            if 0:#(len(mhaste_t)>0) and (haste==mhaste_t[-1]) and (ranged_haste==rhaste_t[-1]) and (t % 120)!=5 and (t % 120)!=5+18 and (t % 120)!=5+20:
                dps = dps_t[-1] # don't need to recalc, nothing changed
            else:
                if self.character.talents.improvedAspectHawk>0:
                    ihawk_time = hawk_uptime(3.0 / ranged_haste)
                else:
                    ihawk_time = 0

                if self.character.gear.use1dur>0:
                    if (t % 120)>=5 and (t % 120)<5+self.character.gear.use1dur:
                        self.character.gear.total_rap = self.character.gear.total_rap + self.character.gear.use1ap
                        self.character.gear.total_map = self.character.gear.total_map + self.character.gear.use1ap
                        self.change_stats()
                        if self.character.gear.use1haste>0:
                            factor = (haste_from_rating + self.character.gear.use1haste/15.8/100) / haste_from_rating
                            haste = haste * factor
                            ranged_haste = ranged_haste * factor
                            haste_from_rating = haste_from_rating * factor
                if self.character.gear.use2dur>0:
                    if (t % 120)>=5+self.character.gear.use1dur and (t % 120)<5+self.character.gear.use1dur+self.character.gear.use2dur:
                        self.character.gear.total_rap = self.character.gear.total_rap + self.character.gear.use2ap
                        self.character.gear.total_map = self.character.gear.total_map + self.character.gear.use2ap
                        self.change_stats()
                        if self.character.gear.use2haste>0:
                            factor = (haste_from_rating + self.character.gear.use2haste/15.8/100) / haste_from_rating
                            haste = haste * factor
                            ranged_haste = ranged_haste * factor
                            haste_from_rating = haste_from_rating * factor
                if (t % 120)>=drum_timing and (t % 120)<(drum_timing+30) and use_drums==2:
                    self.character.gear.total_rap = self.character.gear.total_rap + 60
                    self.character.gear.total_map = self.character.gear.total_map + 60
                    self.change_stats()

                mhastes = [haste]
                rhastes = [ranged_haste]
                uptimes = []

                if haste_proc_uptime!=0:
                    factor = (haste_from_rating + haste_proc/15.8/100) / haste_from_rating
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
                    mutual = haste_proc_uptime*ihawk_time*1.1
                    uptimes = [0, haste_proc_uptime-mutual, ihawk_time-mutual, mutual] # higher simultaneous uptime of both effects
                    uptimes[0] = 1 - sum(uptimes[1:]) # calculate base eWS time

                dps_table = []
                sps_table = []
                rot_table = []


                for n in range(0, len(rhastes)):

                    # find best rotation in loop

                    dps = 0

                    selected = -1

                    for m, rot in enumerate(rotations):
                        self.clear()
                        self.melee.haste = mhastes[n]
                        self.ranged.haste = rhastes[n]
                        self.change_haste()
                        self.add_rotation(rot)
                        if (t % 120)>=5 and (t % 120)<23 and self.character.talents.theBeastWithin:
                            dps_new = self.calc_dps(self.calc_dur(),1.5/1.1) * 1.1
                        else:
                            dps_new = self.calc_dps(self.calc_dur(),1)
                        sps_new = len(rot.replace('w','').replace('r','')) / self.calc_dur()
                        if dps_new>dps:
                            dps = dps_new
                            sps = sps_new
                            selected = m

                    dps_table.append(dps)
                    sps_table.append(sps)
                    rot_table.append(rotations[selected])

                    # end rotation loop

                if self.character.gear.use1dur>0:
                    if (t % 120)>=5 and (t % 120)<5+self.character.gear.use1dur:
                        self.character.gear.total_rap = self.character.gear.total_rap - self.character.gear.use1ap
                        self.character.gear.total_map = self.character.gear.total_map - self.character.gear.use1ap
                        self.change_stats()
                if self.character.gear.use2dur>0:
                    if (t % 120)>=5+self.character.gear.use1dur and (t % 120)<5+self.character.gear.use1dur+self.character.gear.use2dur:
                        self.character.gear.total_rap = self.character.gear.total_rap - self.character.gear.use2ap
                        self.character.gear.total_map = self.character.gear.total_map - self.character.gear.use2ap
                        self.change_stats()
                if (t % 120)>=drum_timing and (t % 120)<(drum_timing+30) and use_drums==2:
                    self.character.gear.total_rap = self.character.gear.total_rap - 60
                    self.character.gear.total_map = self.character.gear.total_map - 60
                    self.change_stats()
            
            self.character.gear.crit_rating -= mt_crit*22.1
            
            weighted_dps = [dps_table[n] * uptimes[n] for n in range(0,len(dps_table))]
            weighted_sps = [sps_table[n] * uptimes[n] for n in range(0,len(sps_table))]

            mhaste_t.append(haste)
            rhaste_t.append(ranged_haste)
            dps_t.append(sum(weighted_dps))
            sps_t.append(sum(weighted_sps))
            rotations_t.append(rot_table)

        sps = sum(sps_t)/len(sps_t)
        return time, dps_t, rhaste_t, mhaste_t, rotations_t, sps
    
    def mean_weights(self, duration, weaving = 0, comp = 0, use_drums = 0, drum_timing = 5, haste_pot = 0):
        
        time, dps_t, rhaste_t, mhaste_t, rotations_t, sps = self.mean_dps(duration, weaving, comp, use_drums, drum_timing, haste_pot, silent = 1)
        base_dps = sum(dps_t)/len(dps_t)
        
        self.character.gear.total_rap += 1
        self.character.gear.total_map += 1
        
        time, dps_t, rhaste_t, mhaste_t, rotations_t, sps = self.mean_dps(duration, weaving, comp, use_drums, drum_timing, haste_pot, silent = 1)
        ap_dps = sum(dps_t)/len(dps_t)
        
        self.character.gear.agi += 1
        
        time, dps_t, rhaste_t, mhaste_t, rotations_t, sps = self.mean_dps(duration, weaving, comp, use_drums, drum_timing, haste_pot, silent = 1)
        agi_dps = sum(dps_t)/len(dps_t)
        
        self.character.gear.total_rap -= 1
        self.character.gear.total_map -= 1
        self.character.gear.agi -= 1
        
        self.character.gear.crit_rating += 1
        
        time, dps_t, rhaste_t, mhaste_t, rotations_t, sps = self.mean_dps(duration, weaving, comp, use_drums, drum_timing, haste_pot, silent = 1)
        cr_dps = sum(dps_t)/len(dps_t)
        
        self.character.gear.crit_rating -= 1
        self.character.gear.haste_rating += 1
        
        time, dps_t, rhaste_t, mhaste_t, rotations_t, sps = self.mean_dps(duration, weaving, comp, use_drums, drum_timing, haste_pot, silent = 1)
        haste_dps = sum(dps_t)/len(dps_t)

        self.character.gear.haste_rating -= 1
        
        ap_weight = ap_dps - base_dps
        agi_weight = agi_dps - base_dps
        cr_weight = cr_dps - base_dps
        haste_weight = haste_dps - base_dps
        
        return ap_weight, agi_weight, cr_weight, haste_weight
        


if __name__ == "__main__":
    r = rotationplot('bm')
    r.init_fig()
    r.add_rotation('asmasasAasas') # 5:5:1:1 french non-weave
    r.complete_fig()