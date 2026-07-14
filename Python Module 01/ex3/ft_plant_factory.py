class Plant:
    def __init__(
        self, name: str, height: float,
        age_days: int, daygrow: float = 1.0
    ) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days
        self.daygrow = daygrow

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 2)}cm, {self.age_days} "
              f"days old")

    def grow(self) -> None:
        self.height += self.daygrow

    def age(self) -> None:
        self.age_days += 1


def main() -> None:
    rose = Plant("Rose", 25.0, 30, 0.8)
    oak = Plant("Oak", 200.0, 365, 0.1)
    cactus = Plant("Cactus", 5.0, 90, 0.2)
    sunflower = Plant("Sunflower", 80.0, 45, 1.5)
    fern = Plant("Fern", 15.0, 120, 0.4)

    print("=== Plant Factory Output ===")
    print("Created:", end=" ")
    rose.show()
    print("Created:", end=" ")
    oak.show()
    print("Created:", end=" ")
    cactus.show()
    print("Created:", end=" ")
    sunflower.show()
    print("Created:", end=" ")
    fern.show()


if __name__ == "__main__":
    main()
