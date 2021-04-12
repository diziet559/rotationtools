import matplotlib.pyplot as plt

class rotationplot:
    # talents - not yet used
    focusedFire = 2
    mortalShots = 5
    serpentsSwiftness = 5
    
    # stats for ranged and melee combat w/ all buffs
    ranged = {'dps': 83.3, 'speed': 3.0, 'ammo_dps': 32,'ap': 2696, 'crit': 39.12, 'crit_mod': 1.3, 'multiplier': 1.02 * 1.04 * (1 + 0.8 * 0.03)**3}
    melee = {'dps': 118.6, 'speed': 3.7, 'ap': 2300, 'crit': 34.12, 'multiplier': 1.02 * 1.04 * (1 + 0.8 * 0.03)**3}
    # multiplier: 2% bm talent, 4% arms warr, 3x 3% FI @80% uptime (averaged out)
    haste = 1.2 * 1.15
    melee_haste = 1
    remaining_armor = 6200 - 3075 - 610 - 800 # base - iEA - FF - CoR
    
    # cd state variables
    gcd_available = 0
    auto_available = 0
    arcane_available = 0
    multi_available = 0
    melee_available = 0
    raptor_available = 0
    current_time = 0
    total_damage = 0
    damage = {'auto': 0, 'steady': 0, 'multi': 0, 'arcane': 0, 'raptor': 0, 'melee': 0}
    counts = {'auto': 0, 'steady': 0, 'multi': 0, 'arcane': 0, 'raptor': 0, 'melee': 0}
    
    # plot variables
    ax = ()
    showlabels = 1 # set to true to show labels on all shots
    autocolor = 'firebrick'
    delaycolor = 'lightcoral'
    steadycolor = 'deepskyblue'
    arcanecolor ='green'
    multicolor = 'red'
    raptorcolor = 'sandybrown'
    
    # annotation string prototypes
    rot_stats = 'Ranged speed: {speed:.1f}\nRanged haste: {haste:.2f}\nDuration: {dur:.2f}'
    dps_stats = 'rAP: {rap:.0f}\nmAP: {map:.0f}\nCrit: {crit:.1f}%\nDPS: {dps:.0f}'
    
    def init_fig(self):
        fig, self.ax = plt.subplots(figsize=(10,5), dpi=150)
        self.clear()
    
    def clear(self):
        self.gcd_available = 0
        self.auto_available = 0
        self.arcane_available = 0
        self.multi_available = 0
        self.melee_available = 0
        self.raptor_available = 0
        self.current_time = 0
        self.total_damage = 0
        self.counts = {'auto': 0, 'steady': 0, 'multi': 0, 'arcane': 0, 'raptor': 0, 'melee': 0}
        self.damage['auto'] = ((self.ranged['dps'] + self.ranged['ammo_dps'])*self.ranged['speed'] \
            + self.ranged['ap']/14*self.ranged['speed']) * self.ranged['multiplier'] * (1 + 1.3 * self.ranged['crit']/100)
        self.damage['steady'] = (self.ranged['dps']*2.8 +150 \
            + self.ranged['ap']*0.2) * self.ranged['multiplier'] * (1 + 1.3 * self.ranged['crit']/100)
        self.damage['multi'] = ((self.ranged['dps'] + self.ranged['ammo_dps'])*self.ranged['speed'] +205 \
            + self.ranged['ap']*0.2) * self.ranged['multiplier'] * (1 + 1.3 * self.ranged['crit']/100)
        self.damage['arcane'] = (273 \
            + self.ranged['ap']*0.15) * self.ranged['multiplier'] * (1 + 1.3 * self.ranged['crit']/100)
        self.damage['raptor'] = (self.melee['dps']*self.melee['speed'] + 170 \
            + self.melee['ap']/14*self.melee['speed']) * self.melee['multiplier'] * (1 + self.melee['crit']/100)
        self.damage['melee'] = (self.melee['dps']*self.melee['speed'] \
            + self.melee['ap']/14*self.melee['speed']) * self.melee['multiplier'] * ((0.75 + 0.25*0.65) + self.melee['crit']/100)
    
    def calc_dps(self):
        #end_time = max(self.auto_available, self.multi_available, self.arcane_available, self.melee_available, self.raptor_available)
        end_time = self.auto_available
        self.dps = self.total_damage / end_time * (1 - (self.remaining_armor / ((467.5 * 70) + self.remaining_armor - 22167.5)))
        return self.dps
    
    def complete_fig(self):
        self.ax.set_ylim(0, 3)
        self.ax.set_yticks([0.5, 1.5, 2.5])
        self.ax.set_yticklabels(['Auto', 'Cast', 'GCD'])
        self.ax.set_xlabel('time [s]')
        colors = {'auto':self.autocolor, 'auto delay':self.delaycolor, \
                  'steady':self.steadycolor, 'arcane':self.arcanecolor, \
                  'multi':self.multicolor, 'raptor/melee':self.raptorcolor}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels, bbox_to_anchor=(1.01, 1), loc='upper left')
        self.calc_dps()
        breakdown = ''
        for cast in ('auto', 'steady', 'multi', 'arcane', 'raptor', 'melee'):
            if self.counts[cast] > 0:
                part_dps = self.counts[cast] * self.damage[cast] / self.total_damage
                breakdown = breakdown + cast + ': ' + str(self.counts[cast]) + ' (' + '{part:.1f}'.format(part=100*part_dps) + '%)\n'
        rota = self.rot_stats.format(speed = self.ranged['speed'], haste = self.haste, dur=self.auto_available)
        plt.annotate(rota,(1.01,0.5), xycoords='axes fraction')
        stats = self.dps_stats.format(rap=self.ranged['ap'],map=self.melee['ap'],crit=self.ranged['crit'],dps=self.dps)
        #plt.annotate(stats,(1.01,0.3), xycoords='axes fraction')
        plt.annotate(breakdown,(1.01,-0.02), xycoords='axes fraction')
        plt.show()

    def add_auto(self):
        if (self.auto_available >= self.current_time):
            self.current_time = self.auto_available
        else:
            self.ax.bar(self.auto_available, 0.2, self.current_time-self.auto_available, 0.4, facecolor='white', edgecolor='lightcoral', align='edge')
            if self.showlabels:
                plt.annotate('{delay:.2f}'.format(delay=self.current_time-self.auto_available), (self.current_time-0.02, 0.25), ha='right', va='center')
        if self.showlabels:
            plt.annotate('as', (self.current_time+0.25/self.haste, 0.5), ha='center', va='center')
        self.ax.bar(self.current_time, 0.8, 0.5/self.haste, 0.1, facecolor='white', edgecolor='firebrick', align='edge')
        self.current_time = self.current_time + 0.5/self.haste
        self.auto_available = self.current_time + (self.ranged['speed']-0.5)/self.haste
        self.total_damage = self.total_damage + self.damage['auto']
        self.counts['auto'] = self.counts['auto'] + 1
        
    def add_gcd(self):
        if (self.gcd_available > self.current_time):
            # wait for gcd if not yet up
            self.current_time = self.gcd_available
        # draw gcd rectangle (default: black)
        self.ax.bar(self.current_time, 0.8, 1.5, 2.1, facecolor='white', edgecolor='black', align='edge')
    
    def add_steady(self):
        self.add_gcd()
        self.ax.bar(self.current_time, 0.8, 1.5/self.haste, 1.1, facecolor='white', edgecolor=self.steadycolor, align='edge')
        if self.showlabels:
            plt.annotate('SS', (self.current_time+0.75/self.haste, 1.5), ha='center', va='center')
        self.gcd_available = self.current_time + 1.5
        self.current_time = self.current_time + 1.5/self.haste
        self.total_damage = self.total_damage + self.damage['steady']
        self.counts['steady'] = self.counts['steady'] + 1

    def add_multi(self):
        self.add_gcd()
        if self.multi_available>self.current_time:
            self.current_time = self.multi_available
        self.ax.bar(self.current_time, 0.8, 0.5/self.haste, 1.1, facecolor='white', edgecolor=self.multicolor, align='edge')
        if self.showlabels:
            plt.annotate('MS', (self.current_time+0.25/self.haste, 1.5), ha='center', va='center')
        self.gcd_available = self.current_time +1.5
        self.current_time = self.current_time + 0.5/self.haste
        self.multi_available = self.current_time + 10
        self.total_damage = self.total_damage + self.damage['multi']
        self.counts['multi'] = self.counts['multi'] + 1

    def add_arcane(self):
        self.add_gcd()
        if self.arcane_available>self.current_time:
            self.current_time = self.arcane_available
        self.ax.bar(self.current_time, 0.8, 0.1, 1.1, facecolor='white', edgecolor=self.arcanecolor, align='edge')
        if self.showlabels:
            plt.annotate('Ar', (self.current_time+0.05/self.haste, 1.5), ha='center', va='center')
        self.gcd_available = self.current_time + 1.5
        self.current_time = self.current_time + 0.1
        self.arcane_available = self.current_time + 6
        self.total_damage = self.total_damage + self.damage['arcane']
        self.counts['arcane'] = self.counts['arcane'] + 1
        
    def add_melee(self):
        print(self.current_time)
        if self.melee_available>self.current_time:
            self.current_time = self.melee_available
        self.ax.bar(self.current_time, 0.8, 0.4, 1.1, facecolor='white', edgecolor=self.raptorcolor, align='edge')
        if self.showlabels:
            plt.annotate('MW', (self.current_time+0.2, 1.5), ha='center', va='center')
        self.current_time = self.current_time + 0.4
        self.melee_available = self.current_time + self.melee['speed']/self.melee_haste
        self.total_damage = self.total_damage + self.damage['melee']
        self.counts['melee'] = self.counts['melee'] + 1

    def add_raptor(self):
        print(self.current_time)
        if self.melee_available>self.current_time:
            self.current_time = self.melee_available
        if self.raptor_available>self.current_time:
            self.current_time = self.raptor_available
        self.ax.bar(self.current_time, 0.8, 0.4, 1.1, facecolor='white', edgecolor=self.raptorcolor, align='edge')
        if self.showlabels:
            plt.annotate('MW', (self.current_time+0.2, 1.5), ha='center', va='center')
        self.current_time = self.current_time + 0.4
        self.raptor_available = self.current_time + 6
        self.melee_available = self.current_time + self.melee['speed']/self.melee_haste
        self.total_damage = self.total_damage + self.damage['raptor']
        self.counts['raptor'] = self.counts['raptor'] + 1
        
    def add_rotation(self, s):
        for c in s:
            if c=='a':
                self.add_auto()
            elif c=='A':
                self.add_arcane()
            elif c=='s':
                self.add_steady()
            elif c=='m':
                self.add_multi()
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