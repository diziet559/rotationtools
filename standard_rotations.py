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

# %% BM, with rapid fire
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.5 * 1.3# serpent + quiver + rapid fire
r.change_haste()
r.add_rotation('asasasamaasasaAa')
r.complete_fig('BM 1:1 with skips')

# %% BM, 2:3
r = rotationtools.rotationplot('bm')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.5 * 1.3 * 1.15# serpent + quiver + rapid fire
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
r.melee.haste = 1.05 * 1.3 * 1.3# drums
r.ranged.haste = r.melee.haste * 1.2 * 1.15 * 1.15 # serpent + quiver + hawk
r.change_haste()
r.add_rotation('asawasasawas')
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
r.add_rotation('asawasa')
r.complete_fig()

# %% SV, short French rotation
r = rotationtools.rotationplot('sv')
r.init_fig()
r.melee.haste = 1.05 # drums
r.ranged.haste = r.melee.haste * 1.15 # quiver only
r.change_haste()
r.add_rotation('asmasasAass')
r.complete_fig()

