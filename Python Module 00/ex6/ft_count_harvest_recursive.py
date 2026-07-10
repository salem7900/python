def ft_count_harvest_recursive() -> None:
    days = int(input("Enter the number of days: "))

    def count_days(current_day):
        if current_day > days:
            print("Harvest time!")
            return
        print("Day " + str(current_day))
        count_days(current_day + 1)

    count_days(1)
