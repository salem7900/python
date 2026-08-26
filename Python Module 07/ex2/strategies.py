#!/usr/bin/env python3
from ex0.creature import Creature
from ex1.capabilities import HealCapability, TransformCapability
from .exceptions import InvalidStrategyError
from .strategy import BattleStrategy
from typing import Protocol, cast


class _TransformingCreature(Protocol):
    """Allows using attack() while also having TransformCapability."""

    def attack(self) -> str: ...
    def transform(self) -> str: ...
    def revert(self) -> str: ...


class _HealingCreature(Protocol):
    """Allows using attack() while also having HealCapability."""

    def attack(self) -> str: ...
    def heal(self) -> str: ...


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' for this normal strategy"
            )
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this aggressive strategy"
            )
        transforming = cast(_TransformingCreature, creature)
        return [
            transforming.transform(),
            transforming.attack(),
            transforming.revert(),
        ]


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this defensive strategy"
            )
        healing = cast(_HealingCreature, creature)
        return [healing.attack(), healing.heal()]
