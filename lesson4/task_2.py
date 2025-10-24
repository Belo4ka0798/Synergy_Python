number = int(input("Введите пятизначное число: "))

# Разбиваем на разряды
units = number % 10
tens = (number // 10) % 10
hundreds = (number // 100) % 10
thousands = (number // 1000) % 10
ten_thousands = number // 10000

print(f"Число: {number}")
print(f"Разряды: {ten_thousands}(десятки тысяч) {thousands}(тысячи) {hundreds}(сотни) {tens}(десятки) {units}(единицы)")

# Вычисления
step1 = tens ** units
step2 = step1 * hundreds
step3 = ten_thousands - thousands
result = step2 / step3

print(f"Шаг 1: {tens} ** {units} = {step1}")
print(f"Шаг 2: {step1} * {hundreds} = {step2}")
print(f"Шаг 3: {ten_thousands} - {thousands} = {step3}")
print(f"Результат: {step2} / {step3} = {result}")