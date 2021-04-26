# talents.py

import weakref
import damage

def getChar(s, pos):
    # return char at position as int or 0 if string too short
    return ((int(s[pos]) if len(s)>pos  else 0))

class Talentbuild:
    def __init__(self, s = ''):
        if s.find('wowhead'):
            self.fromWowHead(s)
        else:
            self.load(s)
    def BM(self, s):
        self.improvedAspectHawk = getChar(s, 0)
        self.focusedFire = getChar(s, 2)
        self.unleashedFury = getChar(s, 8)
        self.ferocity = getChar(s, 10)
        self.animalHandler = getChar(s, 14)
        self.frenzy = getChar(s, 15)
        self.ferociousInspiration = getChar(s, 16)
        self.serpentsSwiftness = getChar(s, 19)
    def MM(self, s):
        self.mortalShots = getChar(s, 1)
        self.improvedHuntersMark = getChar(s, 2)
        self.efficiency = getChar(s, 3)
        self.goForTheThroat = getChar(s, 4)
        self.improvedArcaneShot = getChar(s, 5)
        self.rapidKilling = getChar(s, 7)
        self.lethalShots = getChar(s, 9)
        self.barrage = getChar(s, 12)
        self.combatExperience = getChar(s, 13)
        self.rangedWeaponSpecialization = getChar(s, 14)
        self.masterMarksman = getChar(s, 18)
    def SV(self, s):
        self.monsterSlaying = getChar(s, 0)
        self.humanoidSlaying = getChar(s, 1)
        self.savageStrikes = getChar(s, 3)
        self.surefooted = getChar(s, 11)
        self.survivalInstincts = getChar(s, 13)
        self.killerInstincts = getChar(s, 14)
        self.lightningReflexes = getChar(s, 17)
        
    def load(self, s):
        if (s=='7/20/34') or (s=='sv'):
            self.fromWowHead('https://tbc.wowhead.com/talent-calc/hunter/502-0550201205-333200023103023005103')
        elif s=='0/27/34':
            self.fromWowHead('https://tbc.wowhead.com/talent-calc/hunter/-055220120500302-333200023103023005103')
        elif (s=='41/20/0') or (s=='bm'):
            self.fromWowHead('https://tbc.wowhead.com/talent-calc/hunter/532002005050122431051-0505201205')
        else:
            # reset all to zero
            self.BM('')
            self.MM('')
            self.SV('')
    
    def fromWowHead(self, s):
        t = s.split('/')[-1].split('-')
        self.BM(t[0]) if len(t)<=3 else self.BM(t) # no substrings if only BM talents taken
        self.MM(t[1]) if (len(t)>1 or len(t)>3) else self.MM('') # no substrings if only BM talents taken
        self.SV(t[2]) if (len(t)>2 or len(t)>3) else self.SV('') # only 2 substrings if no points in sv
        
class Gear:
    # numbers taken from seventyupgrades WITHOUT ANY TALENTS SELECTED THERE
    agi = 646
    total_rap = 1816
    total_map = 1758
    crit_rating = 130
    hit_rating = 109
    haste_rating = 0
    t3pc = 0
    d3pc = 4
    dst = 0
    rweapon = damage.Weapon(83.3, 2.9) # sunfury bow
    mweapon = damage.Weapon(118.6, 3.7) # mooncleaver
    def load(self, s):
        self.t3pc = 0
        self.dst = 0
        if s=='sv':
            # https://seventyupgrades.com/set/vhxTGj5rtJavANR4AYjXZf
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 690, 1866, 1799, 75, 57, 0
            self.dst = 1
            self.mweapon = damage.Weapon(114.0, 3.5) # legacy
            self.rweapon = damage.Weapon(83.3, 2.9)
        elif s=='bm':
            # https://seventyupgrades.com/set/oCbtJQp3Wwx6LJcu6bVEzm
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 607, 1823, 1760, 173, 96, 0
            self.dst = 1
            self.mweapon = damage.Weapon(118.6, 3.7)
            self.rweapon = damage.Weapon(83.3, 2.9)
        elif s=='bis2t3':
            # https://seventyupgrades.com/set/oCbtJQp3Wwx6LJcu6bVEzm
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 597, 1787, 1724, 173, 106, 0
            self.t3pc = 2
        elif s=='bm-wb':
            # incl. world boss legs
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 616, 1844, 1781, 173, 84, 0
            self.dst = 1
            self.mweapon = damage.Weapon(118.6, 3.7)
            self.rweapon = damage.Weapon(83.3, 2.9)
        elif s=='bm-primal':
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 529, 1825, 1767, 174, 97, 0
        elif s=='d3t3':
            # https://seventyupgrades.com/set/7SoWG9nknKp79h4cJ5u1ng
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 546, 1668, 1605, 185, 93, 0
            self.t3pc = 4
            self.mweapon = damage.Weapon(118.6, 3.7)
            self.rweapon = damage.Weapon(75.5, 3.0)
        elif s=='d3t3nobs':
            # https://seventyupgrades.com/set/7SoWG9nknKp79h4cJ5u1ng
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 560, 1692, 1629, 137, 112, 0
            self.t3pc = 4
        elif s=='2t3kara':
            # https://seventyupgrades.com/set/swwLZLj86DQVykvqcSP5KA
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 553, 1741, 1678, 200, 93, 0
            self.t3pc = 2
        elif s=='2t3':
            # https://seventyupgrades.com/set/omxwrFns92XxxArA3VA3o1
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 541, 1853, 1790, 161, 75, 0
            self.t3pc = 2
        elif s=='bm-pre':
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 564, 1748, 1685, 190, 95, 0
            self.mweapon = damage.Weapon(118.6, 3.7)
            self.rweapon = damage.Weapon(75.5, 3.0)
        elif s=='bm-pre-nobs':
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 590, 1760, 1697, 138, 114, 0
            self.mweapon = damage.Weapon(118.6, 3.5)
            self.rweapon = damage.Weapon(75.5, 3.0)
            

class Pet:
    avgDmg = 60
    specialAvgDmg = 49
    agi = 128
    strength = 162
    atkspd = 2.0
    cobraReflexes = 1
    family = 'ravager'
    def __init__(self, owner):
        self.owner = weakref.ref(owner)
    def dmgBonus(self):
        if self.family=='ravager':
            return 1.1
        elif self.family=='cat':
            return 1.1
        elif self.family=='windserpent':
            return 1.07
        elif self.family=='sporebat':
            return 1.00
    def specialDmg(self):
        if self.family=='ravager':
            avgDmg = 49 * (1 + 0.5 * 1) # gore has 50% chance for double dmg
        elif self.family=='cat':
            avgDmg = 65 # claw
        elif self.family=='windserpent':
            avgDmg = 108+14 # lightning breath
        elif self.family=='sporebat':
            avgDmg = 0 # no special attack
        return avgDmg
    def buffedStats(self):
        owner_rap = self.owner().buffedStats(1)[2]
        buffs = self.owner().raid.buffs()
        debuffs = self.owner().raid.debuffs()
        strength = (self.strength + 20 + \
            (98 if (self.owner().raid.grp.sham or self.owner().raid.grp.enha) else 0)) \
            * (1.1 if buffs[6] else 1)
        agi = (self.agi + buffs[5] + 20) * (1.1 if buffs[6] else 1) # scroll of agi
        m_ap = strength * 2 + 0.22 * owner_rap + buffs[1] + debuffs[1] + (50 if self.owner().gear.t3pc>=4 else 0)
        crit = agi/25.6 + 2 * self.owner().talents.ferocity + buffs[3] + debuffs[3] - 0.6
        hit = self.owner().talents.animalHandler * 2 + buffs[2] + debuffs[2]
        atkspd = self.atkspd / (1 + self.owner().talents.serpentsSwiftness * 0.04) / (1.3 if self.cobraReflexes else 1)
        multiplier = (0.86 if self.cobraReflexes else 1) * buffs[4] * debuffs[4]
        return m_ap, crit, hit, atkspd, multiplier
    def dps(self):
        stats = self.buffedStats()
        dmg_mult = (1 + 0.04 * self.owner().talents.unleashedFury) * self.dmgBonus() * stats[4] * 1.25 # happiness modifier
        mod_dmg = self.avgDmg + stats[0]/14*self.atkspd * dmg_mult
        hit = min(1, 0.91 + stats[2]/100)
        crit = stats[1] / 100
        hasted_attack = stats[3]
        if self.owner().talents.frenzy>0:
            first_frenzy = 1/(1/hasted_attack + 1/1.5) / (crit * 0.2 * self.owner().talents.frenzy)
            frenzied_attack = hasted_attack / 1.3
            frenzy_drop = (1 - (crit * 0.2 * self.owner().talents.frenzy))**int(8/frenzied_attack + 5 + 1) # 1/atkspd autohits + 5 gore/claw/lightning + 1 kill command
            average_extension = 8/int(8/frenzied_attack + 5 + 1) / crit
            average_length = average_extension / frenzy_drop + 8
            frenzy_uptime = average_length / (average_length + first_frenzy)
            average_frenzied_atkspd = hasted_attack / (1 + frenzy_uptime * 0.3)
        else:
            frenzy_uptime = 0
            average_frenzied_atkspd = hasted_attack
        
        if self.owner().talents.ferociousInspiration>0:
            first_fi = 1/(1/average_frenzied_atkspd + 1/1.5) / crit
            fi_drop = (1 - crit)**int(8/average_frenzied_atkspd + 5 + 1) # 1/atkspd autohits + 5 gore/claw/lightning + 1 kill command
            average_length = average_extension / fi_drop + 10
            fi_uptime = average_length / (average_length + first_fi)
        else:
            fi_uptime = 0
        
        autohit_dps = mod_dmg * (hit - 0.25*0.35 + crit) / average_frenzied_atkspd
        if self.family=='windserpent':
            skill_dps = self.specialDmg() * (0.83 + 0.13 * 0.5) * dmg_mult / 1.5 # low hit, low crit, low crit bonus
        else:
            skill_dps = self.specialDmg() * (hit + crit) * dmg_mult / 1.5
        
        total_dps = (autohit_dps + skill_dps) * (1 + 0.01 * self.owner().talents.ferociousInspiration * fi_uptime)
        return total_dps

class Group:
    feral = 1
    bm = 2
    enha = 1
    ret = 0
    sham = 0 # other than enhance
    warr = 0

class Raidsetup:
    grp = Group()
    paladin = 2 # kings + might buffs
    druid = 1 # gift of the wild
    warlock = 1 # curse of recklessness
    ret = 1
    moonkin = 1 # imp faerie fire debuff
    rogue = 1 # imp expose armor debuff
    arms = 1 # blood frenzy debuff
    warr = 1 # sunder if no rogue, no arms
    
    def debuffs(self):
        r_ap = 0
        m_ap = 0
        crit = 0
        hit = 0
        armor_pen = 0
        multiplier = 1
        if self.ret>0:
            crit = crit + 3 # improved seal of the crusader
        if self.moonkin>0:
            hit = hit + 3 # improved faerie fire
        if self.druid>0:
            armor_pen = armor_pen + 610 # faerie fire
        if self.rogue>0:
            armor_pen = armor_pen + 3075 # improved expose armor
        elif (self.warr>0) or (self.arms>0):
            armor_pen = armor_pen + 2600 # sunder armor, only if no rogue
        if self.warlock>0:
            armor_pen = armor_pen + 800 # curse of recklessness
        if self.arms>0:
            multiplier = multiplier * 1.04 # blood frenzy
        r_ap = r_ap + 440 # hunter's mark
        m_ap = m_ap + 110 # imp hunter's mark
        return (r_ap, m_ap, hit, crit, multiplier, armor_pen)
    
    def buffs(self, pet=0, hunter_rap = 0):
        r_ap = 0
        m_ap = 0
        agi = 0
        hit = 0
        crit = 0
        kings = 0
        multiplier = 1
        if self.grp.feral>0:
            crit = crit + 5
        if (self.grp.sham>0) or (self.grp.enha):
            agi = agi + 88 # grace of air totem
        if self.grp.warr>0:
            m_ap = m_ap + 306 # battle shout
        if (self.druid>0) or (self.grp.feral>0):
            agi = agi + 18
        if (self.paladin>0):
            kings = 1
            if self.paladin>=2:
                m_ap = m_ap + 264
                r_ap = r_ap + 264
        multiplier = multiplier * (1+0.03*0.95)**self.grp.bm
        if not pet:
            r_ap = r_ap + 155 # aspect of the hawk
        if pet:
            m_ap = m_ap + 0.22 * hunter_rap
        return (r_ap, m_ap, hit, crit, multiplier, agi, kings)

class Character:
    gear = Gear()
    raid = Raidsetup()
    talents = Talentbuild()
    usingFlask = 1 # elixir of major agility otherwise
    usingDrums = 0
    
    def __init__(self, spec):
        self.talents.load(spec)
        self.gear.load(spec)
        self.pet = Pet(self)
        if spec=='bm':
            self.raid.grp.bm = max(self.raid.grp.bm - 1, 0)
            self.usingFlask = 1
        else:
            self.usingFlask = 1
        if self.usingDrums:
            self.gear.haste_rating = self.gear.haste_rating + 80
        
    def buffedStats(self, ranged):
        buffs = self.raid.buffs()
        debuffs = self.raid.debuffs()
        # buffs + scroll + food (20 agi each) + elixir if not flasking
        total_agi = (self.gear.agi + buffs[5] + (75 if not self.usingFlask else 40)) \
            * (1.1 if buffs[6] else 1) * (1 + 0.03 * self.talents.lightningReflexes)
        mcrit = total_agi/40 + (self.gear.crit_rating + (0 if self.usingFlask else 20))/22.1 - 1.5 + self.talents.killerInstincts \
            + buffs[3] + debuffs[3]
        rcrit = mcrit + self.talents.mortalShots
        hit = self.talents.surefooted + self.gear.hit_rating/15.8 + buffs[2] + debuffs[2]
        r_ap = self.gear.total_rap - self.gear.agi + total_agi + buffs[0] + (120 if self.usingFlask else 0) + (50 if self.gear.t3pc>=4 else 0)
        m_ap = self.gear.total_map - self.gear.agi + total_agi + buffs[1] + (120 if self.usingFlask else 0) + (50 if self.gear.t3pc>=4 else 0)
        r_ap = r_ap * (1 + 0.02 * self.talents.survivalInstincts) + debuffs[0]
        m_ap = m_ap * (1 + 0.02 * self.talents.survivalInstincts) + debuffs[1]
        #hit = self.gear.hit_rating/15.8 + self.talents.surefooted + debuffs[2]
        haste = (1 + self.gear.haste_rating/15.8/100)
        range_haste = haste * 1.15 * (1 + self.talents.serpentsSwiftness * 0.04)
        hit_mult = min(1, 0.91 + hit/100)
        multiplier = (1 + self.talents.rangedWeaponSpecialization * 0.01) * (1 + self.talents.focusedFire * 0.01) * buffs[4] * debuffs[4] * (1+0.01*self.talents.ferociousInspiration*0.95)
        multiplier = multiplier * hit_mult
        if ranged:
            return (self.gear.rweapon, damage.Ammo(32), r_ap, rcrit, range_haste, multiplier)
        else:
            return (self.gear.mweapon, m_ap, mcrit, haste, multiplier)
        
    def avgRangeDmg(self):
        
        
        return 2696, 39.12, 1.2 * 1.15, 1.02 * 1.04 * (1 + 0.8 * 0.03)**3
        
if __name__ == "__main__":
    c = Character('bm')
    c.gear.load('d3t3')
    print(c.pet.dps())
    