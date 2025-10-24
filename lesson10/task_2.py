# Создаем пустой словарь
my_dict = {}

# Заполняем словарь с помощью цикла
for number in range(10, -6, -1):  # от 10 до -5 включительно
    my_dict[number] = number ** number

# Выводим словарь
print("Получившийся словарь:")
for key, value in my_dict.items():
    print(f"  {key}: {value}")