from ex0 import AquaFactory, CreatureFactory, FlameFactory


def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()

    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(
    factory_a: CreatureFactory,
    factory_b: CreatureFactory,
) -> None:
    creature_a = factory_a.create_base()
    creature_b = factory_b.create_base()

    print(f"{creature_a.describe()} vs. {creature_b.describe()}")
    print("Fight!")
    print(creature_a.attack())
    print(creature_b.attack())


def main() -> None:
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    print("\nTesting factory")
    test_factory(flame_factory)
    print("\nTesting factory")
    test_factory(aqua_factory)

    print("\nTesting battle")
    test_battle(flame_factory, aqua_factory)


if __name__ == "__main__":
    main()
