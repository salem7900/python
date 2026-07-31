#!/usr/bin/env python3
import math


def get_player_pos() -> tuple:
    while True:
        user_input = input("Enter new coordinates "
                           "as floats in format 'x,y,z': ")
        try:
            x_str, y_str, z_str = user_input.split(',')
        except ValueError:
            print("Invalid syntax")
            continue
        coords = []
        error = False
        for value in (x_str.strip(), y_str.strip(), z_str.strip()):
            try:
                coords.append(float(value))
            except ValueError as e:
                print(f"Error on parameter '{value}': {e}")
                error = True
                break
        if error:
            continue
        x, y, z = coords
        return x, y, z


def distance(p1: tuple, p2: tuple) -> float:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def main() -> None:
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    first = get_player_pos()
    print(f"Got a first tuple: {first}")
    print(f"It includes: X={first[0]}, Y={first[1]}, Z={first[2]}")

    center = (0.0, 0.0, 0.0)
    dist_to_center = distance(center, first)
    print(f"Distance to center: {round(dist_to_center, 4)}")

    print("\nGet a second set of coordinates")
    second = get_player_pos()

    dist_between = distance(first, second)
    print(f"\nDistance between the 2 sets of "
          f"coordinates: {round(dist_between, 4)}")


if __name__ == "__main__":
    main()
