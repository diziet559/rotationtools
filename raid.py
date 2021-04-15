# raid.py

class group:
    feral = 1
    bm = 2
    enha = 1
    ret = 0
    sham = 0 # other than enhance
    warr = 0

class raidsetup:
    grp = group()
    paladin = 1 # kings buff
    druid = 1 # gift of the wild
    warlock = 1 # curse of recklessness
    ret = 1
    moonkin = 1 # imp faerie fire debuff
    rogue = 1 # imp expose armor debuff
    arms = 1 # blood frenzy debuff
    warr = 1 # sunder if no rogue, no arms
    