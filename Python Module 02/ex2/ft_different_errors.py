#!/usr/bin/env python3
def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")

    elif operation_number == 1:
        100 / 0

    elif operation_number == 2:
        garden_file = open("/non/existent/file")
        garden_file.close()

    elif operation_number == 3:
        "5" + 3  # type: ignore

    else:
        return


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===\n")

    operation_number = 0
    while operation_number < 5:
        print(f"Testing operation {operation_number}...")
        try:
            garden_operations(operation_number)
            print("Operation completed successfully")
        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as error:
            print(f"Caught {error.__class__.__name__}: {error}")

        operation_number = operation_number + 1

    print("\nAll error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
