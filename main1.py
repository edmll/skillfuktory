def calculate_ticket_cost(quantity):
    total_cost = 0

    for _ in range(quantity):
        age = int(input("Введите возраст посетителя: "))

        if age < 18:
            cost = 0
        elif 18 <= age < 25:
            cost = 990
        else:
            cost = 1390

        total_cost += cost

    if quantity > 3:
        total_cost *= 0.9

    return total_cost

ticket_quantity = int(input("Введите количество билетов: "))
total_cost = calculate_ticket_cost(ticket_quantity)
print("Общая стоимость билетов:", total_cost, "руб.")
