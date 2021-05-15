# talents.py

import weakref
import damage
import yaml

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
        self.bestialDiscipline = getChar(s, 13)
        self.animalHandler = getChar(s, 14)
        self.frenzy = getChar(s, 15)
        self.ferociousInspiration = getChar(s, 16)
        self.serpentsSwiftness = getChar(s, 19)
        self.theBeastWithin = getChar(s, 20)
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
        self.exposeWeakness = getChar(s, 20)
        
    def load(self, s):
        if (s=='7/20/34') or (s=='sv'):
            self.fromWowHead('https://tbc.wowhead.com/talent-calc/hunter/502-0550201205-333200023103023005103')
        elif s=='0/27/34' or (s=='sv2'):
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
    arpen = 0
    t3pc = 0
    d3pc = 4
    dst = 0
    motc = 0
    use1ap = 0
    use2ap = 0
    use1haste = 0
    use2haste = 0
    use1dur = 0
    use2dur = 0
    use1cd = 120
    use2cd = 120
    rweapon = damage.Weapon(83.3, 2.9) # sunfury bow
    mweapon = damage.Weapon(118.6, 3.7) # mooncleaver
    setname = 'P1-BiS'
    rweaponname = 'Sunfury'
    mweaponname = 'Mooncleaver'
    
    def load(self, data, name):
        try:
            d = data['Gearsets'][name]
        except:
            print('Set not found. Aborting.')
            return
        self.agi = d.get('agi', 0)
        self.total_rap = d.get('rap', 0)
        self.total_map = d.get('map', 0)
        self.crit_rating = d.get('cr', 0)
        self.hit_rating = d.get('hr', 0)
        self.haste_rating = d.get('haste', 0)
        self.arpen = d.get('arpen', 0)
        self.t3pc = d.get('t3pc', 0)
        if d.get('d3pc', 0)>=4:
            self.arpen = self.arpen + 600
  
        self.dst = 0
        self.motc = 0
        
        self.changeTrinket1(d.get('trinket1', ''))
        self.changeTrinket1(d.get('trinket2', ''))
        
        if d.get('trinket1', '')=='Hourglass' or d.get('trinket2', '')=='Hourglass':
            self.total_map = self.total_map + 300/60*10 # 1 ppm, 10 sec
            self.total_rap = self.total_rap + 300/60*10 # 1 ppm, 10 sec
        try:
            self.rweapon = damage.Weapon(data['RangedWeapons'][d['weapon']]['dps'], \
                                         data['RangedWeapons'][d['weapon']]['speed'])
            self.mweapon = damage.Weapon(data['Twohanders'][d['twohander']]['dps'], \
                                         data['Twohanders'][d['twohander']]['speed'])
            self.setname = name
            self.rweaponname = d['weapon']
            self.mweaponname = d['twohander']
        except:
            print('Weapon not found.')
            
    def removeWeapon(self, data, wtype):
        if wtype == 'RangedWeapons':
            if len(self.rweaponname)==0:
                print('Could not remove weapon - none equipped.')
                return
            weapon = self.rweaponname
            self.rweaponname = ''
        elif wtype == 'Twohanders':
            if len(self.mweaponname)==0:
                print('Could not remove weapon - none equipped.')
                return
            weapon = self.mweaponname
            self.mweaponname = ''
        else:
            print('Unknown weapon type to remove.')
            return
        self.agi = self.agi - data[wtype][weapon].get('agi', 0)
        self.total_rap = self.total_rap - data[wtype][weapon].get('ap', 0)
        self.total_map = self.total_map - data[wtype][weapon].get('ap', 0)
        self.crit_rating = self.crit_rating - data[wtype][weapon].get('cr', 0)
        self.hit_rating = self.hit_rating - data[wtype][weapon].get('hr', 0)
        self.haste_rating = self.haste_rating - data[wtype][weapon].get('haste', 0)
        
    def addWeapon(self, data, weapon, wtype):
        if wtype == 'RangedWeapons':
            self.removeWeapon(data, wtype)
            self.rweapon = damage.Weapon(data[wtype][weapon]['dps'], \
                                         data[wtype][weapon]['speed'])
            self.rweaponname = weapon
        elif wtype == 'Twohanders':
            self.removeWeapon(data, wtype)
            self.mweapon = damage.Weapon(data[wtype][weapon]['dps'], \
                                         data[wtype][weapon]['speed'])
            self.mweaponname = weapon
        else:
            print('Unknown weapon type to use.')
            return
        self.agi = self.agi + data[wtype][weapon].get('agi', 0)
        self.total_rap = self.total_rap + data[wtype][weapon].get('ap', 0)
        self.total_map = self.total_map + data[wtype][weapon].get('ap', 0)
        self.crit_rating = self.crit_rating + data[wtype][weapon].get('cr', 0)
        self.hit_rating = self.hit_rating + data[wtype][weapon].get('hr', 0)
        self.haste_rating = self.haste_rating + data[wtype][weapon].get('haste', 0)
    def changeTrinket1(self, trink):
        self.use1ap = 0
        self.use1haste = 0
        self.use1dur = 0
        self.use1cd = 0
        if trink == 'Slayers':
            self.use1ap = 260
            self.use1dur = 20
            self.use1cd = 120
        if trink == 'Brooch':
            self.use1ap = 278
            self.use1dur = 20
            self.use1cd = 120
        if trink == 'Abacus':
            self.use1haste = 260
            self.use1dur = 10
            self.use1cd = 120
        if trink == 'DST':
            self.dst = 1
        if trink == 'MotC':
            self.motc = 1
    def changeTrinket2(self, trink):
        self.use2ap = 0
        self.use2haste = 0
        self.use2dur = 0
        self.use2cd = 0
        if trink == 'Slayers':
            self.use2ap = 260
            self.use2dur = 20
            self.use2cd = 120
        if trink == 'Brooch':
            self.use2ap = 278
            self.use2dur = 20
            self.use2cd = 120
        if trink == 'Abacus':
            self.use2haste = 260
            self.use2dur = 10
            self.use2cd = 120
        if trink == 'DST':
            self.dst = 1
        if trink == 'MotC':
            self.motc = 1


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
        if self.family in ['cat', 'ravager', 'raptor', 'bat']:
            return 1.1
        elif self.family in ['owl', 'windserpent', 'spider']:
            return 1.07
        elif self.family in ['sporebat', 'wolf']:
            return 1.00
    def specialDmg(self):
        if self.family=='ravager':
            avgDmg = 49 * (1 + 0.5 * 1) # gore has 50% chance for double dmg
        elif self.family in ['cat', 'raptor']:
            avgDmg = 65 # claw
        elif self.family in ['owl', 'bat']:
            avgDmg = 47 # screech
        elif self.family=='windserpent':
            avgDmg = 108+14 # lightning breath
        elif self.family in ['spider', 'wolf']:
            avgDmg = 120 # bite
        elif self.family=='sporebat':
            avgDmg = 0 # no special attack
        return avgDmg
    def specialCD(self):
        if self.family in ['cat', 'raptor', 'owl', 'windserpent', 'bat', 'ravager']:
            return 1.5
        elif self.family in ['wolf', 'spider']:
            return 10
        
    def buffedStats(self):
        owner_rap = self.owner().buffedStats(1)[2]
        buffs = self.owner().raid.buffs()
        debuffs = self.owner().raid.debuffs()
        owner_rap = owner_rap - debuffs[0] - self.owner().gear.motc * 150 - self.owner().raid.ewAP
        strength = (self.strength + 20 + \
            (98 if (self.owner().raid.grp.sham or self.owner().raid.grp.enha) else 0)) \
            * (1.1 if buffs[6] else 1)
        agi = (self.agi + buffs[5] + 20) * (1.1 if buffs[6] else 1) # scroll of agi
        m_ap = strength * 2 + 0.22 * owner_rap + buffs[1] + debuffs[1] + (50 if self.owner().gear.t3pc>=4 else 0) + self.owner().raid.ewAP + (60 if self.owner().usingDrums==2 else 0)
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
        kc_dps = (mod_dmg + 127) * (hit + crit) / 6
        focus_regen = 25 / 4 * (1 + self.owner().talents.bestialDiscipline/2)
        owner_crit = self.owner().buffedStats(1)[3]
        gftt_focus = owner_crit/100 * 25 * self.owner().talents.goForTheThroat # assuming 1 attack per second
        focus_avail = focus_regen + gftt_focus
        min_period = 25 / focus_avail
        if self.family=='windserpent':
            min_period = min_period * 2 # LB uses 50 focus
            skill_dps = self.specialDmg() * (0.84 + 0.13 * 0.5) * dmg_mult / max(self.specialCD(), min_period) # low hit, low crit, low crit bonus
        else:
            skill_dps = self.specialDmg() * (hit + crit) * dmg_mult / max(self.specialCD(), min_period)
        
        total_dps = (autohit_dps + kc_dps + skill_dps) * (1 + 0.01 * self.owner().talents.ferociousInspiration * fi_uptime)
        return total_dps

class Group:
    feral = 1
    bm = 2
    enha = 1
    ret = 0
    sham = 0 # other than enhance
    warr = 0
    def load(self, s):
        self.feral = s.count('f')
        self.bm = s.count('b')
        self.enha = s.count('e')
        self.sham = s.count('s')
        self.warr = s.count('w')
        self.ret = s.count('r')

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
    
    ewAP = 0
    def load(self, s, g=None):
        if g:
            self.grp.load(g)
        pass
    def empty(self):
        self.grp.feral = 0
        self.grp.enha = 0
        self.grp.warr = 0
        self.grp.sham = 0
        self.grp.ret = 0
        self.grp.bm = 0
        self.paladin = 0
        self.druid = 0
        self.warlock = 0
        self.ret = 0
        self.moonkin = 0
        self.rogue = 0
        self.arms = 0
        self.warr = 0
    
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
        if self.druid>0 or self.moonkin>0:
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
        if (self.grp.enha):
            agi = agi + 88*1.15 # improved grace of air totem
        elif (self.grp.sham>0):
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
        multiplier = multiplier * (1+0.03*0.95)**self.grp.bm * (1.02 if self.grp.ret else 1)
        if not pet:
            r_ap = r_ap + 155 # aspect of the hawk
        if pet:
            m_ap = m_ap + 0.22 * hunter_rap
        return (r_ap, m_ap, hit, crit, multiplier, agi, kings)

class Character:
    gear = Gear()
    raid = Raidsetup()
    talents = Talentbuild()
    usingFlask = 0 # elixir of major agility otherwise
    usingDrums = 0 # 1 haste drums, 2 ap drums
    
    def __init__(self, spec):
        self.talents.load(spec)
        #self.gear.load(spec)
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
        total_agi = self.buffedAgi()
        mcrit = total_agi/40 + (self.gear.crit_rating + (0 if self.usingFlask else 20))/22.1 - 1.5 + self.talents.killerInstincts \
            + buffs[3] + debuffs[3]
        rcrit = mcrit + self.talents.mortalShots
        hit = self.talents.surefooted + self.gear.hit_rating/15.8 + buffs[2] + debuffs[2]
        r_ap = self.gear.total_rap - self.gear.agi + total_agi + buffs[0] + (120 if self.usingFlask else 0) + (50 if self.gear.t3pc>=4 else 0)
        m_ap = self.gear.total_map - self.gear.agi + total_agi + buffs[1] + (120 if self.usingFlask else 0) + (50 if self.gear.t3pc>=4 else 0)
        r_ap = r_ap * (1 + 0.02 * self.talents.survivalInstincts) + debuffs[0] + self.raid.ewAP + (150 if self.gear.motc else 0)
        m_ap = m_ap * (1 + 0.02 * self.talents.survivalInstincts) + debuffs[1] + self.raid.ewAP + (150 if self.gear.motc else 0)
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
    def buffedAgi(self):
        buffs = self.raid.buffs()
        total_agi = (self.gear.agi + buffs[5] + (75 if not self.usingFlask else 40)) \
            * (1.1 if buffs[6] else 1) * (1 + 0.03 * self.talents.lightningReflexes)
        return total_agi
        
                
if __name__ == "__main__":
    c = Character('bm')
    with open('gear.yaml') as f:
        data = yaml.safe_load(f)
    c.gear.load(data, 'D3T3')
    c.raid.ewAP = 0
    print(c.pet.dps())
