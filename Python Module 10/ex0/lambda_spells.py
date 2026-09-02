#!/usr/bin/env python3


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda
                  artifact: artifact['power'], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda artifact: artifact['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: "* " + spell + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    max_power = max(mages, key=lambda mage: mage['power'])['power']
    min_power = min(mages, key=lambda mage: mage['power'])['power']
    avg_power = round(sum(mage['power'] for mage in mages) / len(mages), 2)

    return {
        'max_power': max_power,
        'min_power': min_power,
        'avg_power': avg_power
    }


def main() -> None:
    # Lambda Sanctum Test Data
    artifacts: list[dict] = [
        {'name': 'Water Chalice', 'power': 80, 'type': 'armor'},
        {'name': 'Shadow Blade', 'power': 102, 'type': 'accessory'},
        {'name': 'Ice Wand', 'power': 84, 'type': 'focus'},
        {'name': 'Earth Shield', 'power': 101, 'type': 'armor'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'focus'},
    ]

    mages: list[dict] = [
        {'name': 'Alex', 'power': 93, 'element': 'light'},
        {'name': 'Morgan', 'power': 94, 'element': 'fire'},
        {'name': 'Kai', 'power': 69, 'element': 'fire'},
        {'name': 'Luna', 'power': 65, 'element': 'lightning'},
        {'name': 'Phoenix', 'power': 97, 'element': 'ice'},
    ]

    spells: list[str] = ['fireball', 'darkness', 'lightning', 'heal']

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    for artifact in sorted_artifacts:
        print(
            f"{artifact['name']} ({artifact['power']} power)"
        )

    print("\nTesting power filter...")
    above_power = power_filter(mages, 90)
    for mage in above_power:
        print(f"{mage['name']} ({mage['power']} power)")

    print("\nTesting spell transformer...")
    transformed_spells = spell_transformer(spells)
    for spell in transformed_spells:
        print(spell)

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"Max power: {stats['max_power']}")
    print(f"Min power: {stats['min_power']}")
    print(f"Average power: {stats['avg_power']}")


if __name__ == '__main__':
    main()
