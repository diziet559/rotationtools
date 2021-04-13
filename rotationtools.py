#!/usr/bin/env python3
import matplotlib.pyplot as plt
import damage
import abilities

class rotationplot:
    ranged = damage.AverageRangedDamage(
        damage.Weapon(83.3, 2.9),
        damage.Ammo(23),
        2300,
        30,
        1.02
    )

    melee = damage.AverageMeleeDamage(
        damage.Weapon(118.6, 3.7),
        2000, 25, 1.02
    )

    gcd_available = 0
    auto_available = 0
    current_time = 0
    total_damage = 0
    haste = 1.2 * 1.15 * 1.05
    abilities = abilities.create(haste, ranged, melee)
    ax = ()
    rot_stats = 'Ranged speed: {speed:.1f}\nRanged haste: {haste:.2f}\nDuration: {dur:.2f}'
    dps_stats = 'rAP: {rap:.0f}\nmAP: {map:.0f}\nCrit: {crit:.1f}%\nDPS: {dps:.0f}'
    row0 = {
        'Auto': 0.1,
        'Cast': 1.1,
        'GCD': 2.1,
    }

    def init_fig(self):
        fig, self.ax = plt.subplots(figsize=(20,8), dpi=100)

    def complete_fig(self):
        self.ax.set_xlim(-0.25, 14)
        self.ax.set_ylim(0, 3)
        self.ax.set_yticks([0.5, 1.5, 2.5])
        self.ax.set_yticklabels(self.row0.keys())
        labels = list(self.abilities.keys())
        handles = [plt.Rectangle((0,0),0.75,0.75, color=self.abilities[label].color) for label in labels]
        plt.legend(handles, labels, bbox_to_anchor=(0.85, 1), loc='upper left')
        self.dps = self.total_damage / self.auto_available
        rota = self.rot_stats.format(speed = self.ranged.speed(), haste = self.haste, dur=self.auto_available)
        plt.annotate(rota,(0.85,0.5), xycoords='axes fraction')
        stats = self.dps_stats.format(rap=self.ranged.ap,map=self.melee.ap,crit=self.ranged.crit,dps=self.dps)
        plt.annotate(stats,(0.85,0.3), xycoords='axes fraction')
        #plt.annotate('Range haste: '+str(self.haste),(1.01,0.455), xycoords='axes fraction')
        plt.show()

    def add_ability(self, ability, y1, x0 = None, update_time = True):
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
        if (self.auto_available > self.current_time):
            self.current_time = self.auto_available
        else:
            self.add_ability(
                abilities.auto_delay(self.current_time - self.auto_available),
                0.4, self.auto_available, False
            )

        self.add_ability(self.abilities['auto'], self.row0['Auto'])
        self.auto_available = self.current_time + (self.ranged.speed()-0.5)/self.haste

    def add_gcd_ability(self, ability_name):
        if (self.gcd_available > self.current_time):
            self.current_time = self.gcd_available

        self.add_ability(self.abilities['gcd'], self.row0['GCD'], None, False)
        self.gcd_available = self.current_time + abilities.GCD_DURATION

        self.add_ability(self.abilities[ability_name], self.row0['Cast'])

    def add_raptor(self):
        self.add_ability(self.abilities['raptor'], self.row0['Cast'])

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


if __name__ == "__main__":
    r = rotationplot()
    r.init_fig()
    r.add_rotation('asAarsasmarsas')
    r.complete_fig()
