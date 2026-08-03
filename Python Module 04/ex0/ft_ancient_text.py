#!/usr/bin/env python3
import sys
import typing


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <filename>")
        return

    print("=== Cyber Archives Recovery ===")
    filename = sys.argv[1]
    print(f"Accessing file '{filename}'")
    try:
        file: typing.IO[str] = open(filename, "r")
    except OSError as error:
        print(f"Error opening file '{filename}': {error}")
        return

    print("---")
    content = file.read()
    print(content, end="")
    print("---")
    file.close()
    print(f"File '{filename}' closed.")


if __name__ == "__main__":
    main()
