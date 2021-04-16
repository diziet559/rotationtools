# talents.py

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
#            self.fromWowHead('https://tbc.wowhead.com/talent-calc/hunter/502-0550201205-333200023103023005103')
#        elif s=='0/27/34':
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
    
    def load(self, s):
        if s=='sv':
            # https://seventyupgrades.com/set/vhxTGj5rtJavANR4AYjXZf
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 690, 1866, 1799, 75, 57, 0
        elif s=='bm':
            # https://seventyupgrades.com/set/oCbtJQp3Wwx6LJcu6bVEzm
            self.agi, self.total_rap, self.total_map, self.crit_rating, \
                self.hit_rating, self.haste_rating \
                = 598, 1814, 1756, 173, 96, 0

class Group:
    feral = 1
    bm = 2
    enha = 1
    ret = 0
    sham = 0 # other than enhance
    warr = 0

class Raidsetup:
    grp = Group()
    paladin = 1 # kings buff
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
    
    def buffs(self):
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
        multiplier = multiplier * (1+0.03*0.8)**self.grp.bm
        r_ap = 155 # aspect of the hawk
        return (r_ap, m_ap, hit, crit, multiplier, agi, kings)

class Character:
    gear = Gear()
    raid = Raidsetup()
    talents = Talentbuild()
    usingFlask = 1 # elixier of major agility if not
    
    def __init__(self, spec):
        self.talents.load(spec)
        self.gear.load(spec)
        if spec=='bm':
            self.raid.grp.bm = max(self.raid.grp.bm - 1, 0)
            self.usingFlask = 1
        else:
            self.usingFlask = 0
        
    def buffedStats(self, ranged):
        buffs = self.raid.buffs()
        debuffs = self.raid.debuffs()
        # buffs + scroll + food (20 agi each) + elixir if not flasking
        total_agi = (self.gear.agi + buffs[5] + (75 if not self.usingFlask else 40)) \
            * (1.1 if buffs[6] else 1) * (1 + 0.03 * self.talents.lightningReflexes)
        mcrit = total_agi/40 + (self.gear.crit_rating + 0 if self.usingFlask else 20)/22.1 - 1.5 + self.talents.killerInstincts \
            + buffs[3] + debuffs[3]
        rcrit = mcrit + self.talents.mortalShots
        r_ap = self.gear.total_rap - self.gear.agi + total_agi + buffs[0] + (120 if self.usingFlask else 0)
        m_ap = self.gear.total_map - self.gear.agi + total_agi + buffs[1] + (120 if self.usingFlask else 0)
        r_ap = r_ap * (1 + 0.02 * self.talents.survivalInstincts) + debuffs[0]
        m_ap = m_ap * (1 + 0.02 * self.talents.survivalInstincts) + debuffs[1]
        #hit = self.gear.hit_rating/15.8 + self.talents.surefooted + debuffs[2]
        haste = (1 + self.gear.haste_rating/15.8)
        range_haste = haste * 1.15 * (1 + self.talents.serpentsSwiftness * 0.04)
        multiplier = (1 + self.talents.rangedWeaponSpecialization * 0.01) * (1 + self.talents.focusedFire * 0.01) * buffs[4] * debuffs[4] * (1+0.01*self.talents.ferociousInspiration*0.8)
        if ranged:
            return (damage.Weapon(83.3, 3.0), damage.Ammo(32), r_ap, rcrit, range_haste, multiplier)
        else:
            return (damage.Weapon(118.6, 3.7), m_ap, mcrit, haste, multiplier)
        
    def avgRangeDmg(self):
        
        
        return 2696, 39.12, 1.2 * 1.15, 1.02 * 1.04 * (1 + 0.8 * 0.03)**3
        
if __name__ == "__main__":
    c = Character('sv')
    c.buffedStats(1)