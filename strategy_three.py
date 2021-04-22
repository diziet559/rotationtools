from collections import namedtuple
from itertools import product
from dataclasses import dataclass, field
from math import ceil
from typing import List, Dict, Tuple
from PIL import Image, ImageDraw
from copy import deepcopy

base_weapon_speed = 2.9
haste = 3.36

@dataclass
class Action:
    damage: float
    cast: float
    cooldown: float

def new_actions():
    actions: Dict[str, Action] = {  # damage,             cast,           cooldown
        "auto":   Action(1400,  .5 / haste,     (base_weapon_speed - .5) / haste),
        "steady": Action(1500,  1.5 / haste,    0),
        "multi":  Action(1600,  .5 / haste,     10),
        "arcane": Action(800,   0,              6)
    }
    return actions

def new_cds(actions=None) -> Dict[str, float]:
    if actions is None:
        actions = new_actions()
    cooldowns = {action: 0 for action in actions.keys()}
    cooldowns["GCD"] = 0
    return cooldowns

@dataclass
class Rotation:
    damage: float = 0
    time: float = 0
    cast_sequence: List[str] = field(default_factory=list)
    cast_log: List[Tuple[float, str]] = field(default_factory=list)
    actions: Dict[str, Action] = field(default_factory=new_actions)
    cooldowns: Dict[str, float] = field(default_factory=new_cds)

    def update_rotation(self, action: str):
        self.damage += self.actions[action].damage
        self.cast_sequence.append(action)

        wait = max(self.cooldowns[action], 0 if action == "auto" else self.cooldowns["GCD"])
        self.time += wait
        self.cast_log.append((self.time, action + "_started"))
        self.advance_cooldowns(wait)

        if action != "auto":
            self.cooldowns["GCD"] = 1.5

        self.time += self.actions[action].cast
        self.cast_log.append((self.time, action + "_finished"))
        self.advance_cooldowns(self.actions[action].cast)

        self.cooldowns[action] = self.actions[action].cooldown  # cooldown

    def advance_cooldowns(self, time):
        for a, cd in self.cooldowns.items():
            self.cooldowns[a] = max(0, cd - time)

    def delay_if_cast(self, action: str) -> float:
        wait = max(self.cooldowns[action], 0 if action == "auto" else self.cooldowns["GCD"])
        return max((wait + self.actions[action].cast) - self.cooldowns["auto"], 0)

    def print_cast_log(self):
        for k, v in r.cast_log:
            print(k, v)


def strategy_three(steps=20) -> Rotation:
    """
    Greedily compare GCD value vs delaying a shots value
    """
    rotation = Rotation()
    auto_dps = rotation.actions["auto"].damage / rotation.actions["auto"].cooldown
    steady_dps = rotation.actions["steady"].damage / 1.5

    rotation.update_rotation("auto")
    for step in range(1, steps):
        last_pass_length = len(rotation.cast_sequence)
        for action in ("steady", "multi", "arcane"):
            auto_value_lost = auto_dps * rotation.delay_if_cast(action)
            wasted_GCD = max((rotation.cooldowns["auto"] + rotation.actions["auto"].cast) - rotation.cooldowns["GCD"], 0)
            GCD_value_gained = wasted_GCD * steady_dps

            if auto_value_lost <= GCD_value_gained / 4:
                rotation.update_rotation(action)
                break

        if len(rotation.cast_sequence) == last_pass_length:
            rotation.update_rotation("auto")

    return rotation

r = strategy_three()
print(r.cast_sequence)