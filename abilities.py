# abilities.py

ABILITIES_TO_TALLY = ['auto', 'steady', 'multi', 'arcane', 'raptor', 'melee']
GCD_DURATION = 1.5

class Tally(dict):
    def __init__(self,*arg,**kw):
        super(Tally, self).__init__(*arg, **kw)
        self.reset()

    def add(self, ability):
        if (ability in ABILITIES_TO_TALLY):
            self[ability] = self[ability] + 1

    def reset(self):
        for ability in ABILITIES_TO_TALLY:
            self[ability] = 0

    def breakdown(self, total_damage, abilities):
        for cast in ABILITIES_TO_TALLY:
            if self[cast] > 0:
                cast_dmg_pct = (self[cast] * abilities[cast].damage) / total_damage
                breakdown = breakdown + cast + ': ' + str(self[cast]) + ' (' + '{part:.1f}'.format(part=100*cast_dmg_pct) + '%)\n'


class Ability:
    def __init__(self, color, damage, duration, height = 0.8):
        self.height = height
        self.duration = duration
        self.damage = damage
        self.color = color

def create(haste, ranged, melee):
    return {
        'auto': Ability('firebrick', ranged.auto(), 0.5 / haste),
        'steady': Ability('deepskyblue', ranged.steady(), 1.5 / haste),
        'gcd': Ability('black', 0, GCD_DURATION),
        'multi': Ability('red', ranged.multi(), 0.5 / haste),
        'arcane': Ability('green', ranged.arcane(), 0.1),
        'raptor': Ability('sandybrown', melee.raptor(), 0.4),
        'melee': Ability('sandybrown', melee.auto(), 0.4),
        'autodelay': Ability('lightcoral', 0, 0), # for legend purposes only
    }

def auto_delay(time):
    return Ability('lightcoral', 0, time, 0.2)
