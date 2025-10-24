# Ввод количества чисел
N = int(input("Введите количество чисел: "))

# Счетчик нулей
zero_count = 0

# Ввод N чисел и подсчет нулей
for i in range(N):
    number = int(input(f"Введите число {i+1}: "))
    if number == 0:
        zero_count += 1

# Вывод результата
print(f"Количество чисел, равных нулю: {zero_count}")