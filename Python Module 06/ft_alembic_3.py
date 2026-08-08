#!/usr/bin/env python3
from alchemy import elements


def main() -> None:
    print("=== Alembic 3 ===")
    print("Accessing alchemy/elements.py using 'import ...' structure")
    res = elements.create_air()
    print(f"Testing create_air: {res}")


if __name__ == "__main__":
    main()
