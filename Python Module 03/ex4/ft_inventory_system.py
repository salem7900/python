#!/usr/bin/env python3
import sys


def parse_arguments(args: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for arg in args:
        parts = arg.split(":")
        if len(parts) != 2 or parts[0] == "":
            print(f"Error - invalid parameter '{arg}'")
            continue
        name, quantity_str = parts
        if name in inventory.keys():
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            quantity = int(quantity_str)
        except ValueError as error:
            print(f"Quantity error for '{name}': {error}")
            continue
        inventory.update({name: quantity})
    return inventory


def max_min_quantity(inventory: dict[str, int]) -> None:
    names = list(inventory.keys())
    quants = list(inventory.values())
    max = 0
    min = 0
    i = 0
    while i < len(quants):
        if quants[max] < quants[i]:
            max = i
        if quants[min] > quants[i]:
            min = i
        i += 1
    print(
        f"Item most abundant: {names[max]} "
        f"with quantity {quants[max]}"
    )
    print(
        f"Item least abundant: {names[min]} "
        f"with quantity {quants[min]}"
    )


def main() -> None:
    print("=== Inventory System Analysis ===")
    inventory = parse_arguments(sys.argv[1:])
    print("Got inventory: ", inventory)

    item_list = list(inventory.keys())
    print(f"Item list: {item_list}")

    total_items = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total_items}")

    if total_items > 0:
        for name, quantity in inventory.items():
            percent = round((quantity / total_items) * 100, 1)
            print(f"Item {name} represents {percent}%")
        max_min_quantity(inventory)

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
