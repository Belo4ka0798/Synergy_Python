# Ввод первого списка
list1_input = input("Введите первый список чисел через пробел: ")
list1 = list(map(int, list1_input.split()))

# Ввод второго списка
list2_input = input("Введите второй список чисел через пробел: ")
list2 = list(map(int, list2_input.split()))

# Проверка размеров списков
if len(list1) > 100000 or len(list2) > 100000:
    print("Ошибка: каждый список может содержать не более 100000 чисел")
    exit()

# Находим пересечение множеств
set1 = set(list1)
set2 = set(list2)
common_numbers = set1 & set2

# Вывод результата
print(f"Количество чисел, содержащихся в обоих списках: {len(common_numbers)}")