import rotationtools

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
        
        base_dps, ap_weight, agi_weight, crit_weight, haste_weight = r.statweights()
        
        base_str = 'Base dps: {dps:.0f}\nStat weights: AP {ap:.2f}, Agi {agi:.2f}, Crit rating {cr:.2f}, Haste rating {haste:.2f}'
        print(base_str.format(dps=base_dps, ap=ap_weight, agi=agi_weight, cr=crit_weight, haste=haste_weight))