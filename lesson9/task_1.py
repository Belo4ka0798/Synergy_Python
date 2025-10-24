# Ввод количества чисел
N_input = input("Введите количество чисел N: ")
if not N_input.isdigit():
    print("Ошибка: N должно быть целым числом")
    exit()

N = int(N_input)
if not (1 < N < 100000):
    print("Ошибка: N должно быть в диапазоне 1 < N < 100000")
    exit()

# Ввод чисел
numbers_input = input("Введите числа через пробел: ")
numbers_list = numbers_input.split()

# Проверка количества чисел
if len(numbers_list) != N:
    print(f"Ошибка: введено {len(numbers_list)} чисел вместо {N}")
    exit()

# Преобразование в целые числа с проверкой
numbers = []
for num_str in numbers_list:
    if not num_str.lstrip('-').isdigit():
        print(f"Ошибка: '{num_str}' не является целым числом")
        exit()

    num = int(num_str)
    if abs(num) > 2 * 10 ** 9:
        print(f"Ошибка: число {num} превышает допустимое значение")
        exit()

    numbers.append(num)

# Подсчет уникальных чисел
unique_count = len(set(numbers))

# Вывод результата
print(f"Количество различных чисел: {unique_count}")