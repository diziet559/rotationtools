# abilities.py

ABILITIES_TO_TALLY = ['gcd', 'auto', 'steady', 'multi', 'arcane', 'raptor', 'melee']
ABILITIES_WITH_CD = ['auto', 'gcd', 'arcane', 'multi', 'raptor', 'melee']
GCD_DURATION = 1.5

class Ability:
    def __init__(self, color, damage, duration, cd = None, annotation = None, height = 0.8):
        self.height = height
        self.duration = duration
        self.damage = damage
        self.color = color
        self.cd = cd
        self.annotation = annotation
        self.has_annotation = annotation != None
        self.first_usage = -1
        self.available = 0
        self.count = 0
        self.has_availability = cd != None

    def reset(self):
        self.first_usage = -1
        self.available = 0
        self.count = 0

    def use(self, current_time):
        if self.first_usage < 0:
            self.first_usage = current_time - self.duration

        if self.has_availability:
            self.available = current_time + self.cd

        self.count = self.count + 1


def create_breakdown(abilities, total_damage):
    breakdown = ''

    for cast in ABILITIES_TO_TALLY:
        ability = abilities[cast]
        if ability.count > 0:
            cast_dmg_pct = (ability.count * ability.damage) / total_damage
            breakdown = breakdown + cast + ': ' + str(ability.count) + ' (' + '{part:.1f}'.format(part=100*cast_dmg_pct) + '%)\n'

    return breakdown

def create(ranged, melee):
    return {
        'auto': Ability(
            'firebrick', ranged.auto(),
            0.5 / ranged.haste, (ranged.weapon.speed - 0.5) / ranged.haste, 'as'
        ),
        'steady': Ability('deepskyblue', ranged.steady(), 1.5 / ranged.haste, None, 'SS'),
        'gcd': Ability('black', 0, GCD_DURATION, GCD_DURATION),
        'multi': Ability('red', ranged.multi(), 0.5 / ranged.haste, 10, 'MS'),
        'arcane': Ability('green', ranged.arcane(), 0.1, 6, 'Ar'),
        'raptor': Ability('sandybrown', melee.raptor(), 0.4, 6, 'MW'),
        'melee': Ability(
            'sandybrown', melee.auto(),
            0.4, melee.weapon.speed / melee.haste, 'MW'
        ),
        'autodelay': Ability('lightcoral', 0, 0), # for legend purposes only
    }

def auto_delay(time):
    return Ability('lightcoral', 0, time, None, None, 0.2)
