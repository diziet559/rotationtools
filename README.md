# TBC Hunter rotation overview

### Contents

- [Hunter rotations and haste](#hunter-rotations-and-haste)
- [Rotation details](#rotation-details)
- [Melee weaving](#melee-weaving)
- [Gear used](#gear-used)

#### Other resources

- [Library usage](library)
- [Raid buffs & debuffs](buffs)
- [License](LICENSE) for this overview & the code

## Hunter rotations and haste

In TBC, hunters will be running different rotations based on their current haste level or effective weapon swing. There are different concepts to visualize this: While the most frequently encountered notation is that of effective weapon swing (eWS) which can also be observed intuitively, using the total haste can be advantageous in some situations.

### Static haste

In early TBC, there will be no static haste on gear. Our only source for haste are 15% from quiver and possibly 20% from the BM talent Serpent's Swiftness. Thus, survival hunters start at 15% total haste, which means that they get 15% additional attack during a particular time. Their eWS is

```
eWS = WS / 1.15
```

as this is how haste is applied in World of Warcraft.

For BM hunters, the two sources of haste apply multiplicatively, so their eWS is

```
eWS = WS / 1.15 / 1.2 = WS / 1.38
```

In both cases, `WS` is the original weapon swing time as given in the weapons tooltip.

In most of TBC, hunters will be using weapons with 3.0 tooltip speed. The only exception is P1, where the best weapon (Sunfury Bow of the Phoenix off of Prince Malchezaar) has a 2.9 speed. The best preraid weapon, Wrathtide Longbow, also has a 3.0 speed as most later weapons.

### Introduction to hunter rotations

All the following rotations are based around keeping your GCD used while delaying your Auto Shots (and melees if weaving) as little as possible.  You do not need to memorize each of them if you understand a small bit about some repeating patterns. Multi-Shot and Arcane Shot are useful for getting value from your GCD when casting a steady would delay your auto.  In many of the slower rotations you will see a pattern like `auto - steady - SPELL - auto - steady`.  This occurs when your weapon swing is well slower than 1.5 and you need to fit in 3 GCDs over 2 weapon swings but steadying in place of `SPELL` would delay your auto.  This pattern is the basis of the French rotation (5:5:1:1) and many of its variants. At slightly faster haste you will see a similar pattern: `auto - steady - arcane - auto - multi`.  This accomplishes the same thing (3 GCDs over 2 weapon swings) but when your weapon swing is much closer as you can fit the **casts** of steady + arcane into a 1.5 second gap between the first two autos.

When your ranged weapon swing goes lower than 1.5, you start to use Multi-Shot (and less often, Arcane Shot) to reset your GCD without losing damage.  You'll see this with any polyrhythmic rotation like 5:3 or 3:2.  You are 1:1ing but overtime your GCD and auto drift and you'll eventually need to Auto twice in a row before you cast.  You can Multi-Shot just before this catchup auto to irk out more DPS without further delaying your swing timer. In all of these situations (which describe something like 90% of the ranged rotations) you're using Multi-Shot and Arcane Shot in situations where you have your GCD up but a fully steady cast would delay and incoming auto.  If you have a basic understanding of the haste ranges for these rotations, you only need to watch your swing timer and GCD to figure when to weave a Multi-Shot in according to the above patterns.  **You don't need to memorize the French rotation if you can vibe your way to following some steadys with Mutli-Shots.**

TLDR:

- Only cast steady immediately following an auto.
- Cast multi/arcane tastefully where you cannot fit a steady. - Weave when GCD is up and auto swing isn't ready.
- For bonus points, do this sometimes `auto - steady - SPELL - auto - steady`

### Changing rotations

During a fight, TBC hunters use different rotations depending on their current haste value or effective weapon swing. Stacking all available haste effects, hunter can achieve 3.36 additional haste for a total of 4.64 with BM talents. This pushes the eWS down to 0.62 seconds. This relies on having improved Aspect of the Hawk and the proc of Dragon Spine Trophy up during your own stacked haste effects from Bloodlust, Rapid Fire, Drums of Battle and Haste Potion. This can only happen for a maximum of 10 seconds (shortest duration of these effects) every 10 minutes (longest cd of these effects), but we will be doing huge dps during this time.

Most of the time, we will have much lower haste. This is okay, we can still do top notch dps without this excessive stacking.

#### BM rotations over haste

Here is an overview of available rotations - which will be explained further on - and their relative dps at different haste levels:

![rotations_bm](img/rotations_bm.png)

Drums of battle are only included when a haste potion is used to illustrate the highest levels of haste achievable in phase 1. When using drums of battle at all times in our group, all of the lower haste points move slightly to the right, increasing our dps. This does not change the rotation we should use at any of these common haste points.

#### SV rotations over haste

For survival hunters, the graph looks slightly different due to lower base haste, and as a result the effective weapon swing is always slower:

![rotations_sv](img/rotations_sv.png)

Depending on the phase and current gear, as a survival hunter we may or may not be specced into improved aspect of the hawk, thus this effect may not apply at all.

## Rotation details

### Basic rotations

- [2:1](#21)
- [1:1](#11)
- [1:2](#12)
- [1:3](#13)

All basic rotations use only steady shot for illustration purposes, but in practice should use multi shot instead of a steady shot whenever it is off CD to slightly improve dps.

#### 2:1

Casting two steady shots and one auto shot alternatingly. This is lower dps than the complex rotation for any level of haste, and shouldn't be used. Ever.

Because we don't use, we don't have to draw it either.

#### 1:1



![bm_one_one](img/bm_one_one.png)

This is the most simple rotation possible and can be achieved by using a macro of the form

```
/castsequence !Auto shot, Steady shot
```

This rotation is used at effective weapon swings from 1.3 to 1.6 seconds, where the GCD and auto shot swing line up almost exactly.

#### 1:2

![bm_one_two](img/bm_one_two.png)

At high enough haste, we can let two auto shots through during the GCD of one steady shot.

#### 1:3

![bm_one_three](img/bm_one_three.png)

At even more haste, we can let a third auto shot through between casting steadies. Sadly, these levels are out of reach an phase 1, and can only be reached with static haste gear in later phases.

### Complex rotations

- [The short French rotation (5:4:1:1)](#the-short-french-rotation-5411)
- [The French rotation (5:5:1:1)](#the-french-rotation-5511)
- [The long French rotation (5:6:1:1)](#the-long-french-rotation-5611)
- [The skipping rotation (5:9:1:1)](#the-skipping-rotation-5911)

#### The short French rotation (5:4:1:1)

![sv_french](img/sv_french.png)

This only ever appears for survival hunters without the 20% haste out of the BM talent tree.

#### The French rotation (5:5:1:1)

![bm_french](img/bm_french.png)

The standard rotation for BM hunters and survival hunter with improved Aspect of the Hawk or DST procs active. Compared to the 1:1 rotation, it slightly delays the auto shots to fit additional shots in. The additional shots are only multi and arcane shots due to their lower cast time.

#### The long French rotation (5:6:1:1)

![bm_longfrench](img/bm_longfrench.png)

A slight dps increase over the standard French rotation with Aspect of the Hawk proc for BM hunters is using multi and arcane together to fit just one additional shot in between your autos, instead of the two additional shot of the standard French rotation.

#### The skipping rotation (5:9:1:1)

![bm_skipping](img/bm_skipping.png)

This is a variant of the 1:1 rotation that uses the shorter cast time of multi and arcane shot to let another auto shot through with each of these casts, resulting in 7 casts for every 9 auto shots. This is used for BM hunters with Rapid fire and Hawk proc or Rapid fire and Bloodlust up (shown here).

### Combined rotations

- [2:3](#23)
- [2:5](#25)

Like the basic rotations, the illustrations here use only steady shots, that should be replaced with multi shots whenever possible.

#### 2:3

![bm_two_three](img/bm_two_three.png)

This rotation alternates cycles of 1:1 and 1:2 to better match GCD and weapon swing.

#### 2:5

![bm_two_five](img/bm_two_five.png)

This combines cycles of 1:2 and 1:3 at very high haste - for phase 1, this requires having improved Aspect of the Hawk *and* DST procs during Bloodlust, Rapid fire, drums and haste potion.

## Melee weaving

- [Rotation dps](#melee-weaving-rotations)
- [French weaving (5:5:1:1 3w)](#french-weaving-5511-3w)
- [1:1 half-weave (2:2 1w)](#11-half-weave-22-1w)
- [6:9:1:1 3w](#6911-3w)
- [6:11:1:1 3w](#61111-3w)
- [3:7 2w](#37-2w)

Although it appears like we have less time at high levels of haste, weaving actually becomes easier in TBC mostly due to the removal of the deadzone. When positioned at minimal shooting range all it takes is the tiniest of steps to get into melee range - weaves can be done as quickly as 0.2 seconds for stepping in, using Raptor strike or a melee white hit, and stepping out again. Depending on habit, backpedaling can be a viable mode of movement here because the distance to travel is just so low. Even slow weavers will manage to stay below 0.4 seconds weaving time, so at even at extremely stacked haste it does not interfere with auto shots. An example video of weaving in the TBC Beta by Sixx can be found [in the resources section](#resources).

There will be situations where weaving will not be possible at specific phases of a fight or even for the whole fight due to boss mechanics. In such situations, it may be beneficial to have a ranged-only set without the two-handed weapon, given that better one-handed weapons are available. A first idea for where to weave can be found in the pet damage taken guide [in the resources section](#resources).

With added weaving choosing the right rotation becomes a 2-dimensional problem as we now have to care about both melee and ranged haste. We will focus first on adding all ranged-only haste effects and general haste effects later. This means that we prioritize ranged damage over melee weaving.

#### Melee weaving rotations

![rotations_weaving_bm](img/rotations_weaving_bm.png)

The dotted lines show non-weaving rotation described above, the weaving rotations will be shown in detail further on. The rotation shown here as 2:2 1w is actually a 1:1 rotation with a weave added after every second auto shot. This is due to the fact that quiver, BM talent haste and improved Aspect of the Hawk yields just the right amount of haste to push a 3.0 ranged weapon to exactly have the eWS of a 3.7 nominal speed melee weapon. Here is the one deviation from the diagram above:

*If we have no ranged-only haste effects other than improved Aspect, **and** we have one significant general haste effect (so anything but drums), it is better to do 1:1 with weaving (2:2 1w)*. This reaches its maximum dps with improved Aspect and Bloodlust or DST up, which should be a quite common scenario.

#### French weaving (5:5:1:1 3w)

![bm_french_weaving](img/bm_french_weaving.png)

Use with no haste effect other than Drums of Battle. Do not use under haste.

This is only used with no haste effects or drums only and scales poorly with drums haste, as the rotation is almost gcd-capped and cannot be done much faster. The weaves should alternate between Raptor Strike and melee white hits.

#### 1:1 half-weave (2:2 1w)

![bm_weaving_oneone](img/bm_weaving_oneone.png)

Use with and either DST proc or Bloodlust, optionally improved Aspect of the Hawk and Drums. Also use with improved Aspect of the Hawk only.

This rotation has a 99% auto efficiency for a 2.9 tooltip speed ranged weapon, and 100% weaving efficiency - with a 3.0 speed bow these values turn around. The shots and melee hits almost perfectly align before this rotation gcd-caps at 25% additional haste from a DST proc or Bloodlust . In this range this is a very simple and efficient rotation, although it is slightly below French weaving without any haste.

#### 6:9:1:1 3w

![bm_weaving_6911](img/bm_weaving_6911.png)

Use with Rapid Fire, Rapid Fire and Drums of Battle or Rapid Fire and improved Aspect of the Hawk. 

#### 6:11:1:1 3w

![bm_weaving_61111](img/bm_weaving_61111.png)

Use with Rapid Fire, improved Aspect of the Hawk and Drums of Battle, or Rapid Fire and Bloodlust (Drums optional).

#### 3:7 2w

![bm_weaving_37](img/bm_weaving_37.png)

This is the maximum haste rotation for weaving in phase 1. Use this with at least Rapid Fire, Bloodlust, and improved Aspect of the Hawk, or eWS below 0.94. The example is drawn for an eWS of 0.7.

## Gear used

The rotations and dps numbers presented here are based on optimal gear for phase 1, with the slight change that all sets use two-handed weapons to enable melee weaving. For fights where it is impossible to weave at all, this may be a slight disadvantage due to the fact that fist weapons can use weightstones that give melee and ranged critical strike rating, whereas all reasonable two-handed weapons can only use sharpening stones that give only melee critical strike rating. All sharpening and weightstones also increase weapon damage for melee and ranged combat, although weapon damage does not increase steady shot damage. Obviosly, with two-handed weapons we can also only use one of these stones, whereas with two one-handed weapons we can use two such stones.

### The sets and their stats

- [BM P1 BiS set](https://seventyupgrades.com/set/4dB2vLVYvjV8BENUcoNNdx)
  - Raw stats: 1823 AP (607 Agi), 21.48% Crit, 6.09% Hit 
  - With talents & buffs & debuffs: 3063 AP, 39.79% Crit, hitcapped
- [SV P1 BiS set](https://seventyupgrades.com/set/bnmrrPa2anXUKAhDgNgR8j)
  - Raw stats: 1866 AP (690 Agi), 19.12% Crit, 3.61% Hit
  - With talents & buffs & debuffs: 3375 AP, 44.33% Crit, hitcapped
  - Fully buffed this set has 1101 agility for a bonus of 275 AP from Expose weakness

There is also an [overview of buffs and debuffs](buffs) that we can expect in a raid environment. For more info on gear, see also Veramos' sheet and videos [in the resources section](#resources).

### Stat weights

Stat weights are useful to compare individual items that do not greatly change the balance of stats. They are not useful for comparing hugely different sets and can be misleading in such situations. Ideally, each set should be simulated individually. In addition, stat weights can and do change depending on the buffs we have.

With this caveat, stat weights can be calculated for the sets shown here.

### Acknowledgement

This overview would have been impossible to complete without others, especially on the [Classic & TBC Hunter Discord](https://discord.gg/8TVHxRr). In no particular order, thanks go out to Aegeagh, Chitzen, Kanja for inventing the French rotation, Tragnar, BradBlondeBeard, Veramos for gear choices, Ocisly for pushing survival, Wdwune for contributing to the code, Antiserum for discussing weaving rotations, Sixx for weaving, and Bouk who has gone missing recently. This applies to this guide and the library as well.

### Resources

- [Bouk's rotation guide](https://boukx.github.io/rotations/)
- [Kanja's TBC Hunter guide (French)](https://chasseur-bc.jimdofree.com/), the reason it is called the "French" rotation
- [BradBlondeBeard's Burning Book of pet damage taken](https://docs.google.com/spreadsheets/d/1p7vucH8lt0Gjyz-Q75sILextXvu5ZRKt-nZ_MK7e7dE) - can also be used as a guideline of where to weave
- [WatchYourSixx - Weaving on target dummy](https://www.twitch.tv/watchyoursixx/clip/FrailInventiveLarkSquadGoals-RdjmoEbMLQmpvszv) in TBC Beta
- [WatchYourSixx - Weaving on DM:T ghost](https://www.twitch.tv/watchyoursixx/clip/EphemeralTriangularAntelopePeanutButterJellyTime-VzsoK3UXd1V9ebul) in TBC Beta
- [Veramos' gear comparison sheet](https://docs.google.com/spreadsheets/d/17z2w8rrc_nW4TqLkxy0VzHLpkbCcYGtQFGBV3_8FZjs)
- [Veramos' gearing video](https://www.youtube.com/watch?v=RVdBciAUknc) - there are more than just this one