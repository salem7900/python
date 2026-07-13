class Plant:
    def __init__(
        self, name: str, height: float,
        age_days: int, daygrow: float
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

    print("=== Garden Plant Registry ===")
    rose.show()
    for i in range(1, 8):
        print(f"=== Day {i} ===")
        rose.grow()
        rose.age()
        rose.show()
    print(f"Growth this week: {round(rose.daygrow * 7, 2)}cm")


if __name__ == "__main__":
    main()
