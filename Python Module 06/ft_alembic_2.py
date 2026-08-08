#!/usr/bin/env python3
import alchemy.elements


def main() -> None:
    print("=== Alembic 2 ===")
    print("Accessing alchemy/elements.py using 'import ...' structure")
    res = alchemy.elements.create_earth()
    print(f"Testing create_earth: {res}")


if __name__ == "__main__":
    main()
