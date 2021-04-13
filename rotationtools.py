#!/usr/bin/env python3
import matplotlib.pyplot as plt
import damage
import abilities

class rotationplot:
    ranged = damage.AverageRangedDamage(
        damage.Weapon(83.3, 3.0),
        damage.Ammo(32),
        2696,
        39.12,
        1.02 * 1.04 * (1 + 0.8 * 0.03)**3
    )

    melee = damage.AverageMeleeDamage(
        damage.Weapon(118.6, 3.7),
        2300, 34.12, 1.02 * 1.04 * (1 + 0.8 * 0.03)**3
    )

    gcd_available = 0
    auto_available = 0
    current_time = 0
    total_damage = 0
    tally = abilities.Tally()
    haste = 1.2 * 1.15
    melee_haste = 1
    remaining_armor = 6200 - 3075 - 610 - 800 # base - iEA - FF - CoR
    abilities = abilities.create(haste, ranged, melee)
    ax = ()
    showlabels = 1 # set to true to show labels on all shotss
    rot_stats = 'Ranged speed: {speed:.1f}\nRanged haste: {haste:.2f}\nDuration: {dur:.2f}'
    dps_stats = 'rAP: {rap:.0f}\nmAP: {map:.0f}\nCrit: {crit:.1f}%\nDPS: {dps:.0f}'
    row0 = {
        'Auto': 0.1,
        'Cast': 1.1,
        'GCD': 2.1,
    }

    def init_fig(self):
        fig, self.ax = plt.subplots(figsize=(20,8), dpi=100)
        self.clear()

    def clear(self):
        self.gcd_available = 0
        self.auto_available = 0
        self.current_time = 0
        self.total_damage = 0
        self.tally.reset()

    def calc_dps(self):
        #end_time = max(self.auto_available, self.multi_available, self.arcane_available, self.melee_available, self.raptor_available)
        end_time = self.auto_available
        self.dps = self.total_damage / end_time * (1 - (self.remaining_armor / ((467.5 * 70) + self.remaining_armor - 22167.5)))
        return self.dps

    def complete_fig(self):
        self.ax.set_xlim(-0.25, 14)
        self.ax.set_ylim(0, 3)
        self.ax.set_yticks([0.5, 1.5, 2.5])
        self.ax.set_yticklabels(self.row0.keys())
        self.ax.set_xlabel('time [s]')
        labels = list(self.abilities.keys())
        handles = [plt.Rectangle((0,0),1,1, color=self.abilities[label].color) for label in labels]
        plt.legend(handles, labels, bbox_to_anchor=(1.01, 1), loc='upper left')
        self.calc_dps()
        rota = self.rot_stats.format(speed = self.ranged.speed(), haste = self.haste, dur=self.auto_available)
        plt.annotate(rota,(0.85,0.5), xycoords='axes fraction')
        stats = self.dps_stats.format(rap=self.ranged.ap,map=self.melee.ap,crit=self.ranged.crit,dps=self.dps)
        plt.annotate(stats,(0.85,0.3), xycoords='axes fraction')
        plt.annotate(
            self.tally.breakdown(self.total_damage, self.abilities),
            (1.01, -0.02), xycoords='axes fraction'
        )
        #plt.annotate('Range haste: '+str(self.haste),(1.01,0.455), xycoords='axes fraction')
        plt.show()

    def add_ability(self, ability_name, y1, update_time = True):
        self.add_concrete_ability(self.abilities[ability_name], y1, None, update_time)

    def add_concrete_ability(self, ability, y1, x0 = None, update_time = True):
        if (x0 is None):
            x0 = self.current_time

        self.ax.bar(
            x0, ability.height, ability.duration, y1,
            facecolor = 'white',
            edgecolor = ability.color,
            align = 'edge'
        )

        self.total_damage = self.total_damage + ability.damage

        if (update_time):
            self.current_time = self.current_time + ability.duration

    def add_auto(self):
        if (self.auto_available >= self.current_time):
            self.current_time = self.auto_available
        else:
            self.add_concrete_ability(
                abilities.auto_delay(self.current_time - self.auto_available),
                0.4, self.auto_available, False
            )

        self.add_ability('auto', self.row0['Auto'])
        self.auto_available = self.current_time + (self.ranged.speed()-0.5)/self.haste

    def add_gcd_ability(self, ability_name):
        if (self.gcd_available > self.current_time):
            self.current_time = self.gcd_available

        self.add_ability('gcd', self.row0['GCD'], False)
        self.gcd_available = self.current_time + abilities.GCD_DURATION

        self.add_ability(ability_name, self.row0['Cast'])

    def add_raptor(self):
        print(self.current_time)
        self.add_ability('raptor', self.row0['Cast'])

    def add_melee(self):
        print(self.current_time)
        self.add_ability('melee', self.row0['Cast'])

    def add_rotation(self, s):
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
                self.haste = self.haste * 1.15 # manually proc imp hawk for testing


if __name__ == "__main__":
    r = rotationplot()
    r.init_fig()
    #r.add_rotation('asmarsasAawsas') # 5:5:1:1:1:1 french 2-weave
    r.add_rotation('asmasasAasas') # 5:5:1:1:1:1 french 2-weave
    #r.add_rotation('asmarsasAawsasaws') # 6:6:1:1:1:1 french 3-weave
    #r.add_rotation('asAarmasawsasasw') # 5:6:1:1
    #r.add_rotation('asmahrsasawsas') # 5:5:1:1:1:1 hawk after 2nd, skip arcane
    #r.add_rotation('rasaswmasasAwas') # 5:5:1:1:1:1
    #r.add_rotation('amwasaswasaswamaswasaswas') # 1:1 mw
    #r.add_rotation('asasasasasasasasasas') # 1:1 mw
    #r.add_rotation('asmarsasAarsasahsrasasr') # 5:5:1:1:1:1
    #r.add_rotation('asmasasAasas') # 5:5:1:1
    #r.add_rotation('hasmasasasasas') # 6:6:1
    #r.add_rotation('aswasasras')
    #r.add_rotation('asas')
    #r.add_rotation('asmahsasasas') # 5:5:1:1 hawk after 2nd auto -> skip arcane, got to 1:1
    r.complete_fig()
