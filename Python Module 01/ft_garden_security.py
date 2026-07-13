class Plant:
    def __init__(self, name: str, height: float, age_days: int, daygrow: float) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days
        self.daygrow = daygrow
    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 2)}cm, {self.age_days} days old")
    def grow(self) -> None:
        self.height += self.daygrow
    def age(self) -> None:
        self.age_days += 1
    def set_height(self, height: float) -> None:
        self.height = height
    def set_age(self, age_days: int) -> None:
        self.age_days = age_days
    def get_height(self) -> float:
        return self.height
    def get_age(self) -> int:
        return self.age_days

def main() -> None:
    rose = Plant("Rose", 15.0, 10, 0.8)
    original_height = rose.get_height()
    original_age = rose.get_age()

    print(f"=== Garden Security System ===")
    print("Plant created:", end=" ")
    rose.show()
    print()
    rose.set_height(25.0)
    rose.set_age(-1)
    if rose.height < 0.0:
        rose.height = original_height
        print(f"Rose: Error, height can't be negative")
        print(f"Height update rejected")
    else:
        print(f"Height updated: {rose.height}cm")
    if rose.age_days < 0:
        rose.age_days = original_age
        print(f"Rose: Error, age can't be negative")
        print(f"Age update rejected")
    else:
        print(f"Age updated: {rose.age_days} days")

    print("\nCurrent state:", end=" ")
    rose.show()


if __name__ == "__main__":
    main()
