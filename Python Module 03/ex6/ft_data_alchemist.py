#!/usr/bin/env python3
import random


PLAYERS: list[str] = [
    "Alice", "bob", "Charlie", "dylan", "Emma",
    "Gregory", "john", "kevin", "Liam",
]


def main() -> None:
    print("=== Game Data Alchemist ===\n")

    capitalized_names = [name.capitalize() for name in PLAYERS]
    print(f"New list with all names capitalized: {capitalized_names}")

    already_capitalized = [name for name
                           in PLAYERS if name == name.capitalize()]
    print(f"New list of capitalized names only: {already_capitalized}\n")

    scores = {name: random.randint(1, 1000) for name in capitalized_names}
    print(f"Score dict: {scores}")
    average_score = sum(scores.values()) / len(scores)
    print(f"Score average is {round(average_score, 2)}")

    higher_average = {name: score for name, score
                      in scores.items() if score > average_score}
    print(f"High scores: {higher_average}")


if __name__ == '__main__':
    main()
