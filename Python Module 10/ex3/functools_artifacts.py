#!/usr/bin/env python3
import operator
from functools import lru_cache, partial, reduce, singledispatch
from typing import Any, Callable


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    operations: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }

    try:
        func = operations[operation]
    except KeyError as exc:
        raise ValueError(f"Unknown operation: {operation}") from exc

    return reduce(func, spells)


def _base_enchantment(power: int, element: str, target: str) -> str:
    return f"{element} enchantment (power {power}) on {target}"


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:

    return {
        "fire_enchant": partial(base_enchantment, 50, "fire"),
        "ice_enchant": partial(base_enchantment, 50, "ice"),
        "water_enchant": partial(base_enchantment, 50, "water"),
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:

    @singledispatch
    def dispatch(spell: Any) -> str:
        return "Unknown spell type"

    @dispatch.register(int)
    def _(spell: int) -> str:
        return f"{spell} damage"

    @dispatch.register(str)
    def _(spell: str) -> str:
        return spell

    @dispatch.register
    def _(spell: list) -> str:  # type: ignore[type-arg]
        return f"{len(spell)} spells"

    return dispatch


def main() -> None:

    print("Testing spell reducer...")
    spells = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")
    print(f"Min: {spell_reducer(spells, 'min')}")
    try:
        spell_reducer(spells, "error")  # Testa un'operazione non valida
    except ValueError as exc:
        print(f"Error: {exc}")

    print("\nTesting partial enchanter...")
    enchantments = partial_enchanter(_base_enchantment)
    print(enchantments["fire"]("Sword"))
    print(enchantments["ice"]("Shield"))

    print("\nTesting memoized fibonacci...")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")
    print(memoized_fibonacci.cache_info())

    print("\nTesting spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(f"Damage spell: {dispatcher(42)}")
    print(f"Enchantment: {dispatcher('fireball')}")
    print(f"Multi-cast: {dispatcher([1, 2, 3])}")
    print(dispatcher(1.1))


if __name__ == '__main__':
    main()
