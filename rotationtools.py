#!/usr/bin/env python3
import matplotlib.pyplot as plt
import damage
import abilities
import talents

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

    hawk_until = 0

    ax = ()
    showlabels = 1 # set to true to show labels on all shotss
    rot_stats = 'Ranged speed: {speed:.1f}\nRanged haste: {haste:.2f}\nDuration: {dur:.2f}'
    dps_stats = 'rAP: {rap:.0f}\nmAP: {map:.0f}\nCrit: {crit:.1f}%\nDPS: {dps:.0f}\nDMG: {dmg:.0f}'
    row0 = {
        'Auto': 0.1,
        'Cast': 1.1,
        'GCD': 2.1,
    }
    
    def __init__(self, s=None):
        if not s:
            s = 'bm'
        character = talents.Character(s)
        avgRngDmg = character.buffedStats(1)
        self.ranged = damage.AverageRangedDamage(avgRngDmg[0],avgRngDmg[1],avgRngDmg[2],avgRngDmg[3],avgRngDmg[4],avgRngDmg[5])
        avgMeleeDmg = character.buffedStats(0)
        self.melee = damage.AverageMeleeDamage(avgMeleeDmg[0],avgMeleeDmg[1],avgMeleeDmg[2],avgMeleeDmg[3],avgMeleeDmg[4])
        self.abilities = abilities.create(self.ranged, self.melee)
        self.abilities['multi'].damage = self.abilities['multi'].damage * (1 + character.talents.barrage * 0.04)

    def init_fig(self):
        self.clear()
        fig, self.ax = plt.subplots(figsize=(10, 6), dpi=150)

    def clear(self):
        self.rotation_string = ''
        self.current_time = 0
        self.total_damage = 0

        for ability in self.abilities.values():
            ability.reset()

        self.ax = 0
    
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
        self.abilities['melee'].cd = self.melee.weapon.speed / self.melee.haste

    def calc_dur(self):
        self.abilities['gcd'].first_usage = self.abilities['gcd'].first_usage + 1.5 # first usage seems weird for gcd
        return max([
            self.abilities[ability].available - self.abilities[ability].first_usage
            for ability in abilities.ABILITIES_WITH_CD
        ])

    def calc_dps(self, duration):
        return self.total_damage / duration * (1 - (self.remaining_armor / ((467.5 * 70) + self.remaining_armor - 22167.5)))

    def complete_fig(self):
        self.ax.set_xlim(-0.25, 12)
        self.ax.set_ylim(0, 3)
        self.ax.set_yticks([0.5, 1.5, 2.5])
        self.ax.set_yticklabels(self.row0.keys())
        self.ax.set_xlabel('time [s]')
        labels = list(self.abilities.keys())
        handles = [plt.Rectangle((0,0),1,1, color=self.abilities[label].color) for label in labels]
        plt.legend(handles, labels, bbox_to_anchor=(1.005, 1), loc='upper left')
        duration = self.calc_dur()
        dps = self.calc_dps(duration)
        rota = self.rot_stats.format(speed = self.ranged.speed(), haste = self.ranged.haste, dur=duration)
        plt.annotate(rota,(1.005,0.5), xycoords='axes fraction')
        stats = self.dps_stats.format(rap=self.ranged.ap,map=self.melee.ap,crit=self.ranged.crit,dps=dps,dmg=self.total_damage)
        plt.annotate(stats,(1.005,0.3), xycoords='axes fraction')
        plt.annotate(
            abilities.create_breakdown(self.abilities, self.total_damage),
            (1.005, -0.02), xycoords='axes fraction'
        )
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
        print(self.current_time)
        self.add_ability('raptor', self.row0['Cast'])

    def add_melee(self):
        print(self.current_time)
        self.add_ability('melee', self.row0['Cast'])

    def add_rotation(self, s):
        self.rotation_string = s
        for c in s:
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
                self.ranged.haste = self.ranged.haste * 1.15 # manually proc imp hawk for testing


if __name__ == "__main__":
    r = rotationplot('sv')
    r.init_fig()
    #r.add_rotation('as') # 1:1
    r.add_rotation('asmasAasass') # 5:4:1:1 french survival
    #r.add_rotation('asmasasAasas') # 5:5:1:1 french non-weave
    #r.add_rotation('asmarsasAawsas') # 5:5:1:1:1:1 french 2-weave
    #r.add_rotation('asmarsasAawsasaws') # 6:6:1:1:1:1 french 3-weave
    #r.add_rotation('asAarmasawsasasw') # 5:6:1:1
    #r.add_rotation('asmahrsasawsas') # 5:5:1:1:1:1 hawk after 2nd, skip arcane
    #r.add_rotation('rasaswmasasAwas') # 5:5:1:1:1:1
    #r.add_rotation('amwasaswasaswamaswasaswas') # 1:1 mw with multis
    #r.add_rotation('asasasasasasasasasas') # 1:1 mw
    #r.add_rotation('asmarsasAarsasahsrasasr') # 5:5:1:1:1:1
    #r.add_rotation('asmasasAasas') # 5:5:1:1
    #r.add_rotation('hasmasasasasas') # 6:6:1
    #r.add_rotation('aswasasras')

    # r.add_rotation('as')
    #r.add_rotation('asmahsasasas') # 5:5:1:1 hawk after 2nd auto -> skip arcane, got to 1:1
    r.complete_fig()
