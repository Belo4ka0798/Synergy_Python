class Касса:
    def __init__(self, initial_amount=0):
        self.dengi = initial_amount

    def top_up(self, X):
        if X < 0:
            raise ValueError("Нельзя пополнить на отрицательную сумму")
        self.dengi += X
        print(f"Касса пополнена на {X}. Теперь в кассе: {self.dengi}")

    def count_1000(self):
        thousands = self.dengi // 1000
        print(f"В кассе {thousands} целых тысяч")
        return thousands

    def take_away(self, X):
        if X < 0:
            raise ValueError("Нельзя забрать отрицательную сумму")
        if X > self.dengi:
            raise ValueError(f"Недостаточно денег в кассе. В кассе: {self.dengi}, пытаемся забрать: {X}")

        self.dengi -= X
        print(f"Из кассы забрано {X}. Осталось: {self.dengi}")

if __name__ == "__main__":
    # Создаем кассу с начальной суммой 5000
    kassa = Касса(5000)

    # Пополняем кассу на 2500
    kassa.top_up(2500)

    # Проверяем сколько целых тысяч
    kassa.count_1000()  # Выведет: В кассе 7 целых тысяч

    # Забираем 3000 из кассы
    kassa.take_away(3000)

    # Снова проверяем тысячи
    kassa.count_1000()  # Выведет: В кассе 4 целых тысяч

    # Пытаемся забрать слишком много (вызовет ошибку)
    try:
        kassa.take_away(5000)
    except ValueError as e:
        print(f"Ошибка: {e}")