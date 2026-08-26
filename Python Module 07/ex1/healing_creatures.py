#!/usr/bin/env python3
from ex0.creature import Creature
from .capabilities import HealCapability
from typing import Optional


class Sproutling(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Sproutling", "Grass")

    def attack(self) -> str:
        return f"{self.name} uses Vine Whip!"

    def heal(self, target: Optional["HealCapability"] = None) -> str:
        return f"{self.name} heals itself for a small amount"


class Bloomelle(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Bloomelle", "Grass/Fairy")

    def attack(self) -> str:
        return f"{self.name} uses Petal Dance!"

    def heal(self, target: Optional["HealCapability"] = None) -> str:
        return f"{self.name} heals itself and others for a large amount"
