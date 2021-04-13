# rotationtools library
WoW-TBC Hunter rotation tools and visualization

<<<<<<< HEAD
### To run locally
- Install python3
- Install depencencies

```
pip3 install matplotlib
```
=======
## Usage

An instance of the `rotationplot` class has the function `add_rotation()` that accepts strings in the shot notation format defined below. The object will then calculate the duration and damage of this rotation based on current damage stats and current haste. Currently, it does not handle any proc effects, but Improved Aspect of the Hawk procs can be added manually. They do currently not expire.

For an object that has an initialized rotation, `calc_dps()` can be called and returns the dps for this rotation. Also, `calc_dur()` is available and return the duration of this rotation given current haste values. Upon changing haste, `recalc()` can be called to recalculate for different haste and damage stats, but keeping the rotation as is.

For generating rotation plots, `init_fig()` must be called beforehand. Alternatively, `recalc()` can be used after initializing the figure. After either supplying a rotation or calling `recalc()`, `complete_fig()` can be called to add labels and thus finalize the plot.

### Shot notation

- `a` for auto shot
- `s` for steady shot
- `m` for multi shot
- `A` for arcane shot
- `r` for raptor strike
- `w` for melee white hits
- `h` manual Improved Aspect of the Hawk proc

## Usage examples

```python
import rotationtools
r = rotationtools.rotationplot()
r.init_fig()
r.add_rotation('as')
r.complete_fig()
```

This will create the 1:1 rotation example shown below.

![one-one](img/one-one.png)

Simple 1:1 rotation.

```python
import rotationtools
r = rotationtools.rotationplot()
r.init_fig()
r.add_rotation('asmasasAasas')
r.complete_fig()
```

![French rotation](img/french.png)

French rotation (5:5:1:1)
>>>>>>> upstream/main
