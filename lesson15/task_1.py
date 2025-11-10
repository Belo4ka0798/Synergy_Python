class Transport:
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

# Создаем класс Autobus, который наследует от Transport
class Autobus(Transport):
    pass

# Создаем объект Autobus
autobus = Autobus("Renaul Logan", 180, 12)

# Выводим результат
print(f"Название автомобиля: {autobus.name} Скорость: {autobus.max_speed} Пробег: {autobus.mileage}")