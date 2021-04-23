import rotationtools

# %% BM, French rotation
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 # serpent + quiver
r.change_haste()
r.add_rotation('asmasasAasas')
r.complete_fig('BM French rotation')

# %% BM, long French rotation with imp. hawk
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15# serpent + quiver + rapid fire
r.change_haste()
r.add_rotation('asAamasasasas')
r.complete_fig('BM long French rotation with imp. hawk')

# %% BM, skipping rotation with rapid fire
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.5 * 1.15# serpent + quiver + rapid fire
r.change_haste()
r.add_rotation('asasasamaasasaAa')
r.complete_fig('BM 1:1 with skips')

# %% BM, skipping and weaving with rapid fire and hawk
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.5 * 1.15# serpent + quiver + rapidfire + hawk
r.change_haste()
r.add_rotation('asawsasamawasasaAawasa')
r.complete_fig('BM skipping and weaving')

# %% BM, skipping and weaving with lust and drums
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 * 1.3 # drums and lust
r.ranged.haste = r.melee.haste * 1.2 * 1.15# serpent + quiver
r.change_haste()
r.add_rotation('asawsasamawsasasawA')
r.complete_fig('BM 1:1 with weaving')

# %% BM, skipping and weaving with lust and drums
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 * 1.3 # drums and lust
r.ranged.haste = r.melee.haste * 1.2 * 1.15# serpent + quiver
r.change_haste()
r.add_rotation('aswas')
r.complete_fig('BM 1:1 with weaving')

# %% BM, 2:3
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.5 * 1.15# serpent + quiver + rapid fire
r.change_haste()
r.add_rotation('saasa')
r.complete_fig('BM 2:3')

# %% BM, 2:5
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.5 * 1.3 * 1.15 * 1.5# serpent + quiver + rapid fire
r.change_haste()
r.add_rotation('saaasaa')
r.complete_fig('BM 2:5')

# %% BM, French rotation with weaving
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 # serpent + quiver
r.change_haste()
r.add_rotation('asmawsaswasAaws')
r.complete_fig('BM French rotation with weaving')
r.calc_dur()

# %% BM, 1:1 weaving with hawk
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.3 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 # serpent + quiver + hawk
r.change_haste()
r.add_rotation('asasw')
r.complete_fig('BM 1:1 weaving with hawk')

# %% BM, 1:1 weaving with lust
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 * 1.3 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 # serpent + quiver
r.change_haste()
r.add_rotation('asasw')
r.complete_fig('BM 1:1 weaving with hawk')

# %% BM, 1:1 0.33w
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 * 1.3 * 1.3# drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 # serpent + quiver + hawk
r.change_haste()
r.add_rotation('sawasawsaawsa')
r.complete_fig('BM 1:1 weaving with hawk')

# %% BM, 1:1
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 # serpent + quiver + hawk
r.change_haste()
r.add_rotation('asas')
r.complete_fig('BM 1:1')

# %% BM, French rotation with hawk proc
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 # serpent + quiver + hawk proc
r.change_haste()
r.add_rotation('asAamasasasas')
r.complete_fig('BM French rotation with hawk proc')

# %% BM, 1:1 with hawk proc
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 # serpent + quiver + hawk proc
r.change_haste()
r.add_rotation('as')
r.complete_fig('BM 1:1 with hawk proc')

# %% BM, 1:1 with rapid fire and hawk proc
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 * 1.5# serpent + quiver + hawk proc + rapidfire
r.change_haste()
r.add_rotation('asasa')
r.complete_fig('BM 1:1 with rapid fire and hawk proc')

# %% BM, 1:1 with hawk proc
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 2.4
r.ranged.haste = r.melee.haste * 1.2 * 1.15 # serpent + quiver
r.change_haste()
r.add_rotation('saasa')
r.complete_fig('BM 1:1 with hawk proc')
r.calc_dur(1)

# %% BM, max haste, 1:2
r = rotationtools.rotationplot('bm')
r.init_fig()
r.character.gear.total_rap = r.character.gear.total_rap + 278
r.character.gear.total_map = r.character.gear.total_map + 278
r.change_stats()
r.melee.haste = 1.3 * 1.30 # bloodlust + (hastepot+drums)
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 * 1.3 # serpent + quiver + hawk proc + rapidfire
r.change_haste()
for ability in r.abilities:
    r.abilities[ability].damage = r.abilities[ability].damage * 1.1
r.add_rotation('asaasa')
r.complete_fig('BM 1:2 at max haste')

# %% BM, max haste, 1:2
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.3 * 2 # bloodlust + (hastepot+drums) + more
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 * 1.3 # serpent + quiver + hawk proc + rapidfire
r.change_haste()
r.add_rotation('asaaasaa')
r.complete_fig('BM 1:3')

# %% BM, max haste, 3:7 with weaving
r = rotationtools.rotationplot('bm')
r.init_fig()
r.character.gear.total_rap = r.character.gear.total_rap + 278
r.character.gear.total_map = r.character.gear.total_map + 278
r.change_stats()
r.melee.haste = 1.3 * 1.55 # bloodlust + (hastepot+drums+DST)
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 * 1.3 # serpent + quiver + hawk proc + rapidfire
r.change_haste()
for ability in r.abilities:
    r.abilities[ability].damage = r.abilities[ability].damage * 1.1
r.add_rotation('sawasaawasaa')
r.complete_fig('BM 3:7 with weaving at max haste')

# %% SV, short French rotation
r = rotationtools.rotationplot('sv')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.15 # quiver only
r.change_haste()
r.add_rotation('asmasasAass')
r.complete_fig()

# %% SV, French rotation
r = rotationtools.rotationplot('sv')
r.init_fig()
r.melee.haste = 1.05 * 1.3 # drums
r.ranged.haste = r.melee.haste * 1.15 # quiver only
r.change_haste()
r.add_rotation('as')
r.complete_fig()

# %% SV, French rotation
r = rotationtools.rotationplot('sv')
r.init_fig()
r.melee.haste = 1.05 * 1.3 # drums
r.ranged.haste = r.melee.haste * 1.15 # quiver only
r.change_haste()
r.add_rotation('asmasasaAasas')
r.complete_fig()

# %% SV, short French rotation with weaving
r = rotationtools.rotationplot('sv')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.15 # quiver only
r.change_haste()
r.add_rotation('asmawsaswAasaws')
r.complete_fig()

