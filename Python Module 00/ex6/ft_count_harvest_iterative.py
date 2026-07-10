def ft_count_harvest_iterative() -> None:
    days = int(input("Days until harvest: "))
    for i in range(1, days + 1):
        print("Day " + str(i))
    print("Harvest time!")
