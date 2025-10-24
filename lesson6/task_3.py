# Ввод чисел A и B
A = int(input("Введите число A: "))
B = int(input("Введите число B: "))

# Проверка условия A < B
if A >= B:
    print("Ошибка: A должно быть меньше B")
else:
    # Создаем список четных чисел
    even_numbers = []

    # Перебираем числа от A до B
    for number in range(A, B + 1):
        if number % 2 == 0:  # Проверяем четность
            even_numbers.append(str(number))

    # Выводим результат через пробел
    print(" ".join(even_numbers))