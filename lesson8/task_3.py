# Ввод максимальной массы лодки
m_input = input("Введите максимальную массу лодки (1 ≤ m ≤ 1000000): ")
if not m_input.isdigit():
    print("Ошибка: m должно быть целым числом")
    exit()

m = int(m_input)
if not (1 <= m <= 10 ** 6):
    print("Ошибка: m должно быть в диапазоне 1 ≤ m ≤ 1000000")
    exit()

# Ввод количества рыбаков
n_input = input("Введите количество рыбаков (1 ≤ n ≤ 100): ")
if not n_input.isdigit():
    print("Ошибка: n должно быть целым числом")
    exit()

n = int(n_input)
if not (1 <= n <= 100):
    print("Ошибка: n должно быть в диапазоне 1 ≤ n ≤ 100")
    exit()

# Ввод весов рыбаков
weights = []
for i in range(n):
    weight_input = input(f"Введите вес рыбака {i + 1}: ")
    if not weight_input.isdigit():
        print("Ошибка: вес должен быть целым числом")
        exit()

    weight = int(weight_input)
    if not (1 <= weight <= m):
        print(f"Ошибка: вес должен быть в диапазоне 1 ≤ вес ≤ {m}")
        exit()

    weights.append(weight)

# Сортируем веса по возрастанию
weights.sort()

# Алгоритм подсчета лодок
left = 0
right = n - 1
boats = 0

while left <= right:
    # Если самый тяжелый и самый легкий могут пойти вместе
    if left < right and weights[left] + weights[right] <= m:
        left += 1
        right -= 1
    else:
        # Иначе только самый тяжелый
        right -= 1
    boats += 1

# Вывод результата
print(f"Минимальное количество лодок: {boats}")