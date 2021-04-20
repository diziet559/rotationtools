import rotationtools

def getweights(r, pet_mod=1):
    r.change_stats()
    r.recalc()
    base_dps = r.calc_dps(r.calc_dur(), pet_mod)
    
    # increase ap by 1 for ap weight
    r.character.gear.total_rap = r.character.gear.total_rap + 1
    r.character.gear.total_map = r.character.gear.total_map + 1
    r.change_stats()
    r.recalc()
    ap_dps = r.calc_dps(r.calc_dur(), pet_mod)
    
    # also increase agi for agi weight, total ap includes agi already
    r.character.gear.agi = r.character.gear.agi + 1
    r.change_stats()
    r.recalc()
    agi_dps = r.calc_dps(r.calc_dur(), pet_mod)
    
    # undo ap and agi changes
    r.character.gear.total_rap = r.character.gear.total_rap - 1
    r.character.gear.total_map = r.character.gear.total_map - 1
    r.character.gear.agi = r.character.gear.agi - 1
    # increase crit rating by 1 for crit weight
    r.character.gear.crit_rating = r.character.gear.crit_rating + 1
    r.change_stats()
    r.recalc()
    crit_dps = r.calc_dps(r.calc_dur(), pet_mod)
    
    # undo crit rating
    r.character.gear.crit_rating = r.character.gear.crit_rating - 1
    r.change_stats()
    # increase haste for haste rating weight
    r.melee.haste = r.melee.haste * (1+1/15.8/100)
    r.ranged.haste = r.ranged.haste * (1+1/15.8/100)
    r.change_haste()
    r.recalc()
    haste_dps = r.calc_dps(r.calc_dur(), pet_mod)
    
    # calculate stat weights from dps values for each stat
    ap_weight = ap_dps - base_dps
    agi_weight = (agi_dps - base_dps)
    crit_weight = (crit_dps - base_dps)
    haste_weight = (haste_dps - base_dps)
    
    # return to old values
    r.melee.haste = r.melee.haste / (1+1/15.8/100)
    r.ranged.haste = r.ranged.haste / (1+1/15.8/100)
    r.change_haste()
    r.recalc()

    return base_dps, ap_weight, agi_weight, crit_weight, haste_weight
    

if __name__ == "__main__":
    spec_dps = []
    for spec in ['bm', 'sv']:
        labels = []
        rotations = []
        r = rotationtools.rotationplot(spec)
        if spec=='sv':
            r.add_rotation('asmasAasass')
        else:
            r.add_rotation('asmasasAasas')
        
        base_dps, ap_weight, agi_weight, crit_weight, haste_weight = getweights(r)
        
        base_str = 'Base dps: {dps:.0f}\nStat weights: AP {ap:.2f}, Agi {agi:.2f}, Crit rating {cr:.2f}, Haste rating {haste:.2f}'
        print(base_str.format(dps=base_dps, ap=ap_weight, agi=agi_weight, cr=crit_weight, haste=haste_weight))