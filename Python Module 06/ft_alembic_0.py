#!/usr/bin/env python3
import elements


def main() -> None:
    print("=== Alembic 0 ===")
    print("Using: 'import ...' structure to access elements.py")
    res = elements.create_fire()
    print(f"Testing create_fire: {res}")


if __name__ == "__main__":
    main()
