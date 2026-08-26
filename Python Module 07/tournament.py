#!/usr/bin/env python3
from ex0 import AquaFactory, CreatureFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    AggressiveStrategy,
    BattleStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
    NormalStrategy,
)

Opponent = tuple[CreatureFactory, BattleStrategy]


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    creatures = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]

    for i in range(len(creatures)):
        creature_a, strategy_a = creatures[i]
        for j in range(i + 1, len(creatures)):
            creature_b, strategy_b = creatures[j]

            print("\n* Battle *")
            print(f"{creature_a.describe()} vs. "
                  f"{creature_b.describe()} now fight!")
            try:
                for line in strategy_a.act(creature_a):
                    print(line)
                for line in strategy_b.act(creature_b):
                    print(line)
            except InvalidStrategyError as error:
                print(f"Battle error, aborting tournament: {error}")
                return


def main() -> None:
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    battle([
        (flame_factory, normal),
        (healing_factory, defensive),
    ])

    print("\nTournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([
        (flame_factory, aggressive),
        (healing_factory, defensive),
    ])

    print("\nTournament 2 (multiple)")
    print("[ (Aquabub+Normal), (Healing+Defensive), "
          "(Transform+Aggressive) ]")
    battle([
        (aqua_factory, normal),
        (healing_factory, defensive),
        (transform_factory, aggressive),
    ])


if __name__ == "__main__":
    main()
