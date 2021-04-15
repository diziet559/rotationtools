# talents.py

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
        self.serpentsSwiftness = getChar(s, 19)
    def MM(self, s):
        self.mortalShots = getChar(s, 1)
        self.improvedHuntersMark = getChar(s, 2)
        self.efficiency = getChar(s, 3)
        self.goForTheThroat = getChar(s, 4)
        self.improvedArcaneShot = getChar(s, 5)
        self.rapidKilling = getChar(s, 7)
        self.lethalShots = getChar(s, 9)
    def SV(self, s):
        self.monsterSlaying = getChar(s, 0)
        self.humanoidSlaying = getChar(s, 1)
        self.savageStrikes = getChar(s, 3)
        self.surefooted = getChar(s, 12)
        self.survivalInstincts = getChar(s, 14)
        self.killerInstincts = getChar(s, 15)
        self.lightningReflexes = getChar(s, 18)
        
    def load(self, s):
        if s=='7/20/34':
            self.fromWowHead('https://tbc.wowhead.com/talent-calc/hunter/502-0550201205-333200023103023005103')
        elif s=='41/20/0':
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
        