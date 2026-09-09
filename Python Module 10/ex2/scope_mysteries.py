#!/usr/bin/env python3
from collections.abc import Callable


def mage_counter() -> Callable:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable:
    total_power = initial_power

    def addition(added_power: int) -> int:
        nonlocal total_power
        total_power += added_power
        return total_power

    return addition


def enchantment_factory(enchantment_type: str) -> Callable:

    def enchanting_table(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchanting_table


def memory_vault() -> dict[str, Callable]:
    memories: dict[str, object] = {}

    def store(key: str, value: object) -> None:
        memories[key] = value

    def recall(key: str) -> object:
        return memories.get(key, "Memory not found")

    return {"store": store, "recall": recall}


def main() -> None:

    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    addition = spell_accumulator(100)
    print(f"Base 100, add 20: {addition(20)}")
    print(f"Base 100, add 30: {addition(30)}")

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    vault["store"]("secret", 42)
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")


if __name__ == '__main__':
    main()
