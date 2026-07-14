class Plant:
    def __init__(
        self, name: str, height: float = 0.0,
        age_days: int = 0, daygrow: float = 1.0
    ) -> None:
        self.name = name
        self._height = height if height >= 0 else 0.0
        self._age_days = age_days if age_days >= 0 else 0
        self.daygrow = daygrow

    def show(self) -> None:
        print(f"{self.name}: {round(self._height, 2)}cm, "
              f"{self._age_days} days old")

    def grow(self) -> None:
        self._height += self.daygrow

    def age(self) -> None:
        self._age_days += 1

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = height
            print(f"Height updated: {height}cm")

    def set_age(self, age_days: int) -> None:
        if age_days < 0:
            print(f"{self.name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age_days = age_days
            print(f"Age updated: {age_days} days")

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age_days


def main() -> None:
    rose = Plant("Rose", 15.0, 10)

    print("=== Garden Security System ===")
    print("Plant created:", end=" ")
    rose.show()
    print()

    rose.set_height(25.0)
    rose.set_age(30)
    print()

    rose.set_height(-5.0)
    rose.set_age(-1)

    print("\nCurrent state:", end=" ")
    rose.show()


if __name__ == "__main__":
    main()
