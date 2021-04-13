# abilities.py

GCD_DURATION = 1.5

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
        'raptor': Ability('sandybrown', (melee.raptor() + melee.auto()) / 2, 0.4),
        'autodelay': Ability('lightcoral', 0, 0), # for legend purposes only
    }

def auto_delay(time):
    return Ability('lightcoral', 0, time, 0.2)
