def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_sequence(n):
    # Вычисляем факториал исходного числа
    first_factorial = factorial(n)

    # Создаем список факториалов от first_factorial до 1
    result_list = []
    for i in range(first_factorial, 0, -1):
        result_list.append(factorial(i))

    return first_factorial, result_list


number = int(input("Введите натуральное целое число: "))
fact_result, sequence = factorial_sequence(number)

print(f"Факториал числа {number}: {fact_result}")
print(f"Результирующий список: {sequence}")