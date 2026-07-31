#!/usr/bin/env python3
import sys


def main() -> None:
    lista = []
    arguments = sys.argv[1:]
    print("=== Player Score Analytics ===")

    if len(sys.argv) < 2:
        print("No scores provided. Usage: "
              "python3 ft_score_analytics.py <score1> <score2> ...")
        return

    for argument in arguments:
        try:
            score = int(argument)
            lista.append(score)
        except ValueError:
            print(f"Invalid parameter: '{argument}'")

    if lista:
        print(f"\nScores processed: {lista}")
        print(f"Total players: {len(lista)}")
        print(f"Total score: {sum(lista)}")
        print(f"Average score: {(sum(lista) / len(lista)):.2f}")
        print(f"High score: {max(lista)}")
        print(f"Low score: {min(lista)}")
        print(f"Score range: {max(lista) - min(lista)}")


if __name__ == "__main__":
    main()
