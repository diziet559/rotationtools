# ranged.py
class Ammo:
    def __init__(self, dps):
        self.dps = dps

class Weapon:
    def __init__(self, dps, speed):
        self.dps = dps
        self.speed = speed

class Ranged:
    def __init__(self, weapon, ammo, ap, crit, multiplier):
        self.weapon = weapon
        self.ammo = ammo
        self.ap = ap
        self.crit = crit
        self.multiplier = multiplier
        self.crit_dmg_multiplier = 1.3

    def ave_auto(self):
        return self.ave_ranged_attack(0, 1 / 14 * self.weapon.speed)

    def ave_steady(self):
        return self.ave_ranged_attack(150, 0.2, False)

    def ave_multi(self):
        return self.ave_ranged_attack(205, 0.2)

    def ave_arcane(self):
        return (273 + self.ap * 0.15) * self.multiplier * self.ave_crit_dmg_increase()

    def ave_ranged_attack(self, dmg_increase, ap_mod, include_ammo = True):
        weapon_dmg = self.weapon.speed * (
            self.weapon.dps + (self.ammo.dps if include_ammo else 0)
        )

        return (weapon_dmg + dmg_increase + self.ap * ap_mod) * \
            self.multiplier * self.ave_crit_dmg_increase()

    def ave_crit_dmg_increase(self):
        return (1 + self.crit_dmg_multiplier * self.crit / 100)

    def speed(self):
        return self.weapon.speed
