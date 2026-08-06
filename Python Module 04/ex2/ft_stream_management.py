#!/usr/bin/env python3
import sys
import typing


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <filename>")
        return

    print("=== Cyber Archives Recovery & Preservation ===")
    filename = sys.argv[1]
    print(f"Accessing file '{filename}'")
    try:
        file: typing.IO[str] = open(filename, "r")
    except OSError as error:
        print(f"[STDERR] Error opening file '{filename}': {error}",
              file=sys.stderr)
        return

    print("---")
    content = file.read()
    print(content, end="")
    print("---")
    file.close()
    print(f"File '{filename}' closed.")

    print("Transform data:")
    lines = content.splitlines()
    new_content = "".join(line + "#\n" for line in lines)

    print("---")
    print(new_content, end="")
    print("---")

    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    new_filename = sys.stdin.readline().rstrip("\n")

    if not new_filename:
        print("Not saving data.")
        return

    print(f"Saving data to '{new_filename}'")
    try:
        new_file: typing.IO[str] = open(new_filename, "w")
    except OSError as error:
        print(f"[STDERR] Error opening file '{new_filename}': {error}",
              file=sys.stderr)
        print("Data not saved.")
        return

    new_file.write(new_content)
    new_file.close()
    print(f"Data saved in file '{new_filename}'.")


if __name__ == "__main__":
    main()
