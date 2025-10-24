# Ввод последовательности чисел
sequence_input = input("Введите последовательность чисел через пробел: ")
numbers = list(map(int, sequence_input.split()))

# Множество для хранения уже встреченных чисел
seen_numbers = set()

# Список для хранения результатов
results = []

# Проверка каждого числа
for number in numbers:
    if number in seen_numbers:
        results.append("YES")
    else:
        results.append("NO")
        seen_numbers.add(number)

# Вывод результатов
print(" ".join(results))