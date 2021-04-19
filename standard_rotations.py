import rotationtools

# %% BM, French rotation
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 # serpent + quiver
r.change_haste()
r.add_rotation('asmasasAasas')
r.complete_fig('BM French rotation')

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
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 # serpent + quiver + hawk
r.change_haste()
r.add_rotation('aswas')
r.complete_fig('BM 1:1 weaving with hawk')

# %% BM, 1:1
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 # serpent + quiver
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
r.add_rotation('asa')
r.complete_fig('BM 1:2 at max haste')

# %% BM, max haste, 1:2 with weaving
r = rotationtools.rotationplot('bm')
r.init_fig()
r.character.gear.total_rap = r.character.gear.total_rap + 278
r.character.gear.total_map = r.character.gear.total_map + 278
r.change_stats()
r.melee.haste = 1.3 * 1.3 # bloodlust + (hastepot+drums)
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 * 1.3 # serpent + quiver + hawk proc + rapidfire
r.change_haste()
for ability in r.abilities:
    r.abilities[ability].damage = r.abilities[ability].damage * 1.1
r.add_rotation('asarasaasawasa')
r.complete_fig()

# %% SV, short French rotation
r = rotationtools.rotationplot('sv')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.15 # quiver only
r.change_haste()
r.add_rotation('asmasasAasas')
r.complete_fig()

