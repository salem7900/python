#!/usr/bin/env python3
import sys


def main() -> None:
    print("=== Command Quest ===")

    print(f"Program name: {sys.argv[0]}")
    if len(sys.argv) < 2:
        print("No arguments provided!")
        print(f"Total arguments: {len(sys.argv)}")
        return

    n = 1
    print(f"Arguments received: {(len(sys.argv)) - 1}")
    while n < len(sys.argv):
        print(f"Argument {n}: {sys.argv[n]}")
        n += 1

    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()
