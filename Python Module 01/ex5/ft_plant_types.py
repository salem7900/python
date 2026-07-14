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

    def set_height(self, height: float) -> None:
        self.height = height

    def set_age(self, age_days: int) -> None:
        self.age_days = age_days

    def get_height(self) -> float:
        return self.height

    def get_age(self) -> int:
        return self.age_days


class Flower(Plant):
    def __init__(
        self, name: str, height: float,
        age_days: int, daygrow: float, color: str
    ) -> None:
        super().__init__(name, height, age_days, daygrow)
        self.color = color
        self.bloomed = False

    def bloom(self) -> None:
        self.bloomed = True
        print(f"[asking the {self.name} to bloom]")

    def show(self) -> None:
        super().show()
        print(f"Color: {self.color}")
        if self.bloomed:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    def __init__(
        self, name: str, height: float,
        age_days: int, daygrow: float, trunk: float
    ) -> None:
        super().__init__(name, height, age_days, daygrow)
        self.trunk = trunk

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self.trunk}cm")

    def produce_shade(self) -> None:
        print(f"[asking the {self.name} to produce shade]")
        print(f"Tree {self.name} now produces a shade of {self.height}cm "
              f"long and {self.trunk}cm wide.")


class Vegetable(Plant):
    def __init__(
        self, name: str, height: float,
        age_days: int, daygrow: float, season: str
    ) -> None:
        super().__init__(name, height, age_days, daygrow)
        self.season = season
        self.nvalue = 0

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self.season}")
        print(f"Nutritional value: {self.nvalue}")

    def age(self) -> None:
        super().age()
        self.nvalue += 1

    def make_age(self, ndays: int) -> None:
        for i in range(1, ndays + 1):
            self.age()
            super().grow()
        print(f"[make {self.name} grow and age for {ndays} days]")


def main() -> None:
    rose = Flower("Rose", 15.0, 10, 0.8, "red")
    oak = Tree("Oak", 200.0, 365, 0.8, 5.0)
    tomato = Vegetable("Tomato", 5.0, 10, 2.8, "April")

    print("=== Garden Plant Types ===")
    print("=== Flower")
    rose.show()
    rose.bloom()
    rose.show()
    print()
    print("=== Tree")
    oak.show()
    oak.produce_shade()
    print()
    print("=== Vegetable")
    tomato.show()
    tomato.make_age(20)
    tomato.show()


if __name__ == "__main__":
    main()
