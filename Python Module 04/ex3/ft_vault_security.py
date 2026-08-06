#!/usr/bin/env python3


def secure_archive(
    filename: str, action: str = "read", content: str = ""
) -> tuple[bool, str]:
    try:
        if action == "write":
            with open(filename, "w") as file:
                file.write(content)
            return (True, "Content successfully written to file")
        else:
            with open(filename, "r") as file:
                data = file.read()
            return (True, data)
    except OSError as error:
        return (False, f"{error}")


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    result = secure_archive("/not/existing/file")
    print(f"Using 'secure_archive' to read from a nonexistent file: "
          f"\n{result}")

    result = secure_archive("/etc/master.passwd")
    print(f"\nUsing 'secure_archive' to read from an inaccessible file: "
          f"\n{result}")

    result = secure_archive("../ancient_fragment.txt")
    print(f"\nUsing 'secure_archive' to read from a regular file: \n{result}")

    success, content = result
    if success:
        result = secure_archive("new_fragment.txt", "write", content)
        print(f"\nUsing 'secure_archive' to write previous content to a "
              f"new file: \n{result}")


if __name__ == "__main__":
    main()
