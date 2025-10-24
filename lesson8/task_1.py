# Ввод количества чисел
N = int(input("Введите количество чисел N: "))

# Проверка диапазона N
if not (1 < N < 10000):
    print("Ошибка: N должно быть в диапазоне 1 < N < 10000")
    exit()

arr = []

# Ввод N чисел с проверками
for i in range(N):
    try:
        num = int(input())
        # Проверка модуля числа
        if abs(num) > 10**5:
            print(f"Ошибка: число {num} превышает допустимое значение")
            exit()
        arr.append(num)
    except ValueError:
        print("Ошибка: введено не число")
        exit()

# Вывод перевернутого массива
print("Перевернутый массив:")
for num in reversed(arr):
    print(num)