def print_list_recursive(lst):
    # Базовый случай: пустой список
    if not lst:
        print("Конец списка")
        return

    # Выводим первый элемент
    print(f"Элемент: {lst[0]}")

    # Рекурсивный вызов для оставшейся части списка
    print_list_recursive(lst[1:])


# Данный список
my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# Вызов функции
print("Вывод элементов списка рекурсивно:")
print_list_recursive(my_list)