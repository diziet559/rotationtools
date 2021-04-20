import rotationtools

def getweights(r, pet_mod=1):
    r.change_stats()
    r.recalc()
    base_dps = r.calc_dps(r.calc_dur(), pet_mod)
    
    r.character.gear.total_rap = r.character.gear.total_rap + 1
    r.character.gear.total_map = r.character.gear.total_map + 1
    r.change_stats()
    r.recalc()
    ap_dps = r.calc_dps(r.calc_dur(), pet_mod)
    
    r.character.gear.agi = r.character.gear.agi + 1
    r.change_stats()
    r.recalc()
    agi_dps = r.calc_dps(r.calc_dur(), pet_mod)
    
    r.character.gear.total_rap = r.character.gear.total_rap - 1
    r.character.gear.total_map = r.character.gear.total_map - 1
    r.character.gear.agi = r.character.gear.agi - 1
    r.character.gear.crit_rating = r.character.gear.crit_rating + 1
    r.change_stats()
    r.recalc()
    crit_dps = r.calc_dps(r.calc_dur(), pet_mod)
    
    r.character.gear.crit_rating = r.character.gear.crit_rating - 1
    r.change_stats()
    r.melee.haste = r.melee.haste * (1+1/15.8/100)
    r.ranged.haste = r.ranged.haste * (1+1/15.8/100)
    r.change_haste()
    r.recalc()
    haste_dps = r.calc_dps(r.calc_dur(), pet_mod)

    ap_weight = ap_dps - base_dps
    agi_weight = (agi_dps - base_dps)
    crit_weight = (crit_dps - base_dps)
    haste_weight = (haste_dps - base_dps)
    
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