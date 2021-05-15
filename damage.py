# ranged.py
class Ammo:
    def __init__(self, dps):
        self.dps = dps

class Weapon:
    def __init__(self, dps, speed):
        self.dps = dps
        self.speed = speed


class AverageRangedDamage:
    def __init__(self, weapon, ammo, ap, crit, haste, multiplier):
        self.weapon = weapon
        self.ammo = ammo
        self.ap = ap
        self.crit = crit
        self.multiplier = multiplier
        self.haste = haste
        self.crit_dmg_multiplier = 1.3

    def auto(self):
        return self.attack(0, self.weapon.speed / 14)

    def steady(self):
        return self.attack(150, 0.2, False, 2.8)

    def multi(self):
        return self.attack(205, 0.2)

    def arcane(self):
        return (273 + self.ap * 0.15) * self.multiplier * self.damage_from_crit()

    def attack(self, dmg_increase, ap_mod, include_ammo = True, speed_mod = None):
        if speed_mod == None:
            speed_mod = self.weapon.speed

        weapon_dmg = speed_mod * (
            self.weapon.dps + (self.ammo.dps if include_ammo else 0)
        )

        return (weapon_dmg + dmg_increase + self.ap * ap_mod) * \
            self.multiplier * self.damage_from_crit()

    def damage_from_crit(self):
        return (1 + self.crit_dmg_multiplier * self.crit / 100)

    def speed(self):
        return self.weapon.speed

class AverageMeleeDamage:
    def __init__(self, weapon, ap, crit, haste, multiplier):
        self.weapon = weapon
        self.ap = ap
        self.crit = crit
        self.multiplier = multiplier
        self.haste = haste
        self.crit_dmg_multiplier = 1

    def auto(self):
        return self.attack(0, 1 / 14 * self.weapon.speed) * \
            (1 - (0.25 * 0.35) + self.crit / 100 * self.crit_dmg_multiplier)

    def raptor(self):
        return self.attack(170, 1 / 14 * self.weapon.speed) * \
            (1 + self.crit / 100 * self.crit_dmg_multiplier)

    def attack(self, dmg_increase, ap_mod):
        weapon_dmg = self.weapon.speed * self.weapon.dps

        return (weapon_dmg + dmg_increase + self.ap * ap_mod) * self.multiplier

    def speed(self):
        return self.weapon.speed
