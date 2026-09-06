#!/usr/bin/env python3
from typing import Callable, List, Tuple


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} HP"


def lightning(target: str, power: int) -> str:
    return f"Lightning strikes {target} for {power} damage"


def is_powerful_enough(target: str, power: int) -> bool:
    return power >= 20


def spell_combiner(
    spell1: Callable[[str, int], str],
    spell2: Callable[[str, int], str],
) -> Callable[[str, int], Tuple[str, str]]:
    def combined_spell(target: str, power: int) -> Tuple[str, str]:
        result1: str = spell1(target, power)
        result2: str = spell2(target, power)
        return (result1, result2)

    return combined_spell


def power_amplifier(
    base_spell: Callable[[str, int], str],
    multiplier: int,
) -> Callable[[str, int], str]:
    def amplified_spell(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified_spell


def conditional_caster(
    condition: Callable[[str, int], bool],
    spell: Callable[[str, int], str],
) -> Callable[[str, int], str]:
    def conditional_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return conditional_spell


def spell_sequence(
    spells: List[Callable[[str, int], str]],
) -> Callable[[str, int], List[str]]:
    def cast_sequence(target: str, power: int) -> List[str]:
        results: List[str] = [spell(target, power) for spell in spells]
        return results

    return cast_sequence


def demonstrate_spell_combiner(target: str, power: int) -> None:
    print("Testing spell combiner...")
    combined: Callable[[str, int], Tuple[str, str]] = spell_combiner(
        fireball, heal
    )
    result: Tuple[str, str] = combined(target, power)
    print(f"Combined spell result: {result[0]}, {result[1]}")
    print()


def demonstrate_power_amplifier(target: str, power: int) -> None:
    print("Testing power amplifier...")
    multiplier: int = 3
    mega_fireball: Callable[[str, int], str] = power_amplifier(
        fireball, multiplier
    )
    original_result: str = fireball(target, power)
    amplified_result: str = mega_fireball(target, power)
    print(f"Original: {original_result}")
    print(f"Amplified: {amplified_result}")
    print(f"Original power: {power}, "
          f"Amplified power: {power * multiplier}")
    print()


def demonstrate_conditional_caster(
    target: str, strong_power: int, weak_power: int
) -> None:
    print("Testing conditional caster...")
    guarded_lightning: Callable[[str, int], str] = conditional_caster(
        is_powerful_enough, lightning
    )
    strong_result: str = guarded_lightning(target, strong_power)
    weak_result: str = guarded_lightning(target, weak_power)
    print(f"With power {strong_power}: {strong_result}")
    print(f"With power {weak_power}: {weak_result}")
    print()


def demonstrate_spell_sequence(target: str, power: int) -> None:
    print("Testing spell sequence...")
    all_spells: List[Callable[[str, int], str]] = [
        fireball, heal, lightning
    ]
    sequence: Callable[[str, int], List[str]] = spell_sequence(
        all_spells
    )
    results: List[str] = sequence(target, power)
    for line in results:
        print(f"  - {line}")
    print()


def demonstrate_efficiency(target: str, power: int) -> None:
    print("Testing combined efficiency of all spell modifiers...")

    amplified_fireball: Callable[[str, int], str] = power_amplifier(
        fireball, 2
    )
    guarded_amplified: Callable[[str, int], str] = conditional_caster(
        is_powerful_enough, amplified_fireball
    )
    mega_combo: Callable[
        [str, int], Tuple[str, str]
    ] = spell_combiner(guarded_amplified, heal)

    output: Tuple[str, str] = mega_combo(target, power)
    print(f"Mega combo result: {output[0]}, {output[1]}")
    print()


def main() -> None:
    test_values: List[int] = [21, 22, 6]
    test_targets: List[str] = ['Dragon', 'Goblin', 'Wizard', 'Knight']

    demonstrate_spell_combiner(test_targets[0], test_values[0])
    demonstrate_power_amplifier(test_targets[1], test_values[2])
    demonstrate_conditional_caster(
        test_targets[2], test_values[1], test_values[2]
    )
    demonstrate_spell_sequence(test_targets[3], test_values[0])
    demonstrate_efficiency(test_targets[0], test_values[2])


if __name__ == '__main__':
    main()
