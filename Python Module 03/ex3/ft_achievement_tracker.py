#!/usr/bin/env python3
import random

ACHIEVEMENTS: tuple[str, ...] = (
    "Crafting Genius",
    "Strategist",
    "World Savior",
    "Speed Runner",
    "Survivor",
    "Master Explorer",
    "Treasure Hunter",
    "Unstoppable",
    "First Steps",
    "Collector Supreme",
    "Untouchable",
    "Sharp Mind",
    "Boss Slayer",
    "Hidden Path Finder",
)

PLAYER_NAMES: tuple[str, ...] = ("Alice", "Bob", "Charlie", "Dylan")


def gen_player_achievements() -> set[str]:
    nb_achievements = random.randint(1, len(ACHIEVEMENTS))
    achievements: set[str] = set()
    while len(achievements) < nb_achievements:
        achievements.add(random.choice(ACHIEVEMENTS))
    return achievements


def build_players(names: tuple[str, ...]) -> dict[str, set[str]]:
    players: dict[str, set[str]] = {}
    for name in names:
        players[name] = gen_player_achievements()
    return players


def get_all_achievements(players: dict[str, set[str]]) -> set[str]:
    all_achievements: set[str] = set()
    for achievement in players.values():
        all_achievements = all_achievements.union(achievement)
    return all_achievements


def get_common_achievements(players: dict[str, set[str]]) -> set[str]:
    common: set[str] = set()
    is_first = True
    for achievements in players.values():
        if is_first:
            common = achievements
            is_first = False
        else:
            common = common.intersection(achievements)
    return common


def get_exclusive_achievements(
    players: dict[str, set[str]], name: str
) -> set[str]:
    exclusive: set[str] = players[name]
    for other_name, achievements in players.items():
        if other_name != name:
            exclusive = exclusive.difference(achievements)
    return exclusive


def get_missing_achievements(
    players: dict[str, set[str]], name: str, all_achievements: set[str]
) -> set[str]:
    return all_achievements.difference(players[name])


def main() -> None:
    print("=== Achievement Tracker System ===\n")
    players = build_players(PLAYER_NAMES)

    for name in PLAYER_NAMES:
        print(f"Player {name}: {players[name]}")
    print()

    all_achievements = get_all_achievements(players)
    print(f"All distinct achievements: {all_achievements}\n")

    common_achievements = get_common_achievements(players)
    print(f"Common achievements: {common_achievements}\n")

    for name in PLAYER_NAMES:
        exclusive_achievements = get_exclusive_achievements(players, name)
        print(f"Only {name} has: {exclusive_achievements}")
    print()

    for name in PLAYER_NAMES:
        missing_achievements = (
            get_missing_achievements(players, name, all_achievements))
        print(f"{name} is missing: {missing_achievements}")


if __name__ == "__main__":
    main()
