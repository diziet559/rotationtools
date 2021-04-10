import matplotlib.pyplot as plt

class rotationplot:
    range_speed = 2.9
    gcd_available = 0
    auto_available = 0
    current_time = 0
    haste = 1.2 * 1.15 * 1.05
    autocolor = 'firebrick'
    delaycolor = 'lightcoral'
    steadycolor = 'deepskyblue'
    arcanecolor ='green'
    multicolor = 'red'
    raptorcolor = 'sandybrown'
    ax = ()
    rot_stats = 'Ranged speed: {speed:.1f}\nRanged haste: {haste:.2f}\nDuration: {dur:.2f}'
    dps_stats = 'rAP: {rap:.0f}\nmAP: {map:.0f}\nCrit: {crit:.1f}%\nDPS: {dps:.0f}'
    
    def init_fig(self):
        fig, self.ax = plt.subplots(figsize=(10,5), dpi=150)
        
    def complete_fig(self):
        self.ax.set_ylim(0, 3)
        self.ax.set_yticks([0.5, 1.5, 2.5])
        self.ax.set_yticklabels(['Auto', 'Cast', 'GCD'])
        colors = {'auto':self.autocolor, 'auto delay':self.delaycolor, \
                  'steady':self.steadycolor, 'arcane':self.arcanecolor, \
                  'multi':self.multicolor, 'raptor/melee':self.raptorcolor}         
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.legend(handles, labels, bbox_to_anchor=(1.01, 1), loc='upper left')
        rota = self.rot_stats.format(speed = self.range_speed, haste = self.haste, dur=self.auto_available)
        plt.annotate(rota,(1.01,0.5), xycoords='axes fraction')
        stats = self.dps_stats.format(rap=2300,map=2000,crit=30,dps=0)
        plt.annotate(stats,(1.01,0.3), xycoords='axes fraction')
        #plt.annotate('Range haste: '+str(self.haste),(1.01,0.455), xycoords='axes fraction')
        plt.show()

    def add_auto(self):
        if (self.auto_available > self.current_time):
            self.current_time = self.auto_available
        else:
            self.ax.bar(self.auto_available, 0.2, self.current_time-self.auto_available, 0.4, facecolor='white', edgecolor='lightcoral', align='edge')
        self.ax.bar(self.current_time, 0.8, 0.5/self.haste, 0.1, facecolor='white', edgecolor='firebrick', align='edge')
        self.current_time = self.current_time + 0.5/self.haste
        self.auto_available = self.current_time + (self.range_speed-0.5)/self.haste
        
    def add_gcd(self):
        self.ax.bar(self.current_time, 0.8, 1.5, 2.1, facecolor='white', edgecolor='black', align='edge')
    
    def add_steady(self):
        if (self.gcd_available > self.current_time):
            self.current_time = self.gcd_available
        self.add_gcd()
        self.ax.bar(self.current_time, 0.8, 1.5/self.haste, 1.1, facecolor='white', edgecolor=self.steadycolor, align='edge')
        self.gcd_available = self.current_time + 1.5
        self.current_time = self.current_time + 1.5/self.haste

    def add_multi(self):
        if (self.gcd_available > self.current_time):
            self.current_time = self.gcd_available
        self.add_gcd()
        self.ax.bar(self.current_time, 0.8, 0.5/self.haste, 1.1, facecolor='white', edgecolor=self.multicolor, align='edge')
        self.gcd_available = self.current_time +1.5
        self.current_time = self.current_time + 0.5/self.haste

    def add_arcane(self):
        if (self.gcd_available > self.current_time):
            self.current_time = self.gcd_available
        self.add_gcd()
        self.ax.bar(self.current_time, 0.8, 0.1, 1.1, facecolor='white', edgecolor=self.arcanecolor, align='edge')
        self.gcd_available = self.current_time + 1.5
        self.current_time = self.current_time + 0.1
        
    def add_raptor(self):
        self.ax.bar(self.current_time, 0.8, 0.4, 1.1, facecolor='white', edgecolor=self.raptorcolor, align='edge')
        self.current_time = self.current_time + 0.4
        
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


if __name__ == "__main__":
    r = rotationplot()
    r.init_fig()
    r.add_rotation('asAarsasmarsas')
    print(r.auto_available)
    print(r.gcd_available)
    r.complete_fig()