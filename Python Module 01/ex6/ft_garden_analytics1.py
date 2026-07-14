class Plant:
    class Statistics:
        def __init__(self) -> None:
            self.n_grow = 0
            self.n_age = 0
            self.n_show = 0

    def __init__(
        self, name: str, height: float,
        age_days: int, daygrow: float
    ) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days
        self.daygrow = daygrow
        self.stats = self.Statistics()

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 2)}cm, {self.age_days} "
              f"days old")
        self.stats.n_show += 1

    def grow(self) -> None:
        self.height += self.daygrow
        self.stats.n_grow += 1
        print(f"[asking the {self.name} to grow]")

    def age(self) -> None:
        self.age_days += 1
        self.stats.n_age += 1
        print(f"[asking the {self.name} to age]")

    def set_height(self, height: float) -> None:
        self.height = height

    def set_age(self, age_days: int) -> None:
        self.age_days = age_days

    def get_height(self) -> float:
        return self.height

    def get_age(self) -> int:
        return self.age_days

    @staticmethod
    def check_year(n_age: int) -> bool:
        if n_age < 365:
            return False
        else:
            return True

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0, 0.0)


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


class Seed(Flower):
    def __init__(
        self, name: str, height: float,
        age_days: int, daygrow: float, color: str
    ) -> None:
        super().__init__(name, height, age_days, daygrow, color)
        self.nseed = 0

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self.nseed}")

    def bloom(self) -> None:
        super().bloom()
        self.nseed = 42


class Tree(Plant):
    class Statistics(Plant.Statistics):
        def __init__(self) -> None:
            super().__init__()
            self.n_shade = 0

    def __init__(
        self, name: str, height: float,
        age_days: int, daygrow: float, trunk: float
    ) -> None:
        super().__init__(name, height, age_days, daygrow)
        self.trunk = trunk
        self.stats: Tree.Statistics = self.Statistics()

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self.trunk}cm")

    def produce_shade(self) -> None:
        print(f"[asking the {self.name} to produce shade]")
        print(f"Tree {self.name} now produces a shade of {self.height}cm "
              f"long and {self.trunk}cm wide.")
        self.stats.n_shade += 1


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


def display_stats(plant: Plant) -> None:
    print(f"[statistics for {plant.name}]")
    print(f"Stats: {plant.stats.n_grow} grow, {plant.stats.n_age} "
          f"age, {plant.stats.n_show} show")
    if isinstance(plant, Tree):
        print(f"{plant.stats.n_shade} shade")


def main() -> None:
    rose = Flower("Rose", 15.0, 10, 0.8, "red")
    oak = Tree("Oak", 200.0, 365, 0.8, 5.0)
    tomato = Vegetable("Tomato", 5.0, 10, 2.8, "April")
    sunflower = Seed("Sunflower", 80.0, 45, 1.2, "yellow")
    unknown = Plant.anonymous()

    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.check_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.check_year(400)}")
    print()
    print("=== Flower")
    rose.show()
    display_stats(rose)
    rose.grow()
    rose.bloom()
    rose.show()
    display_stats(rose)
    print()
    print("=== Tree")
    oak.show()
    display_stats(oak)
    oak.produce_shade()
    display_stats(oak)
    print()
    print("=== Seed")
    sunflower.show()
    sunflower.age()
    sunflower.grow()
    sunflower.bloom()
    sunflower.show()
    display_stats(sunflower)
    print()
    print("=== Vegetable")
    tomato.show()
    display_stats(tomato)
    print()
    print("=== Anonymous ===")
    unknown.show()
    display_stats(unknown)


if __name__ == "__main__":
    main()
