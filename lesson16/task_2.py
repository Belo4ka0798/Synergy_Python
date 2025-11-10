import random

class Черепашка:
    def __init__(self, x=None, y=None, s=1):
        self.x = random.randint(-10, 10) if x is None else x
        self.y = random.randint(-10, 10) if y is None else y
        self.s = s

    def go_up(self):
        self.y += self.s
        print(f"Идем вверх. Новая позиция: ({self.x}, {self.y})")

    def go_down(self):
        self.y -= self.s
        print(f"Идем вниз. Новая позиция: ({self.x}, {self.y})")

    def go_left(self):
        self.x -= self.s
        print(f"Идем влево. Новая позиция: ({self.x}, {self.y})")

    def go_right(self):
        self.x += self.s
        print(f"Идем вправо. Новая позиция: ({self.x}, {self.y})")

    def evolve(self):
        self.s += 1
        print(f"Эволюция! Теперь шаг: {self.s}")

    def degrade(self):
        if self.s <= 1:
            raise ValueError("s не может стать ≤ 0")
        self.s -= 1
        print(f"Деградация! Теперь шаг: {self.s}")

    def count_moves(self, x2, y2):
        dx = abs(x2 - self.x)
        dy = abs(y2 - self.y)

        # Вычисляем количество ходов по каждой оси
        moves_x = (dx + self.s - 1) // self.s  # округление вверх
        moves_y = (dy + self.s - 1) // self.s  # округление вверх

        # Общее количество ходов - сумма ходов по осям
        total_moves = moves_x + moves_y

        print(f"Минимальное количество ходов до ({x2}, {y2}): {total_moves}")
        return total_moves

    def get_position(self):
        return self.x, self.y

if __name__ == "__main__":
    turtle = Черепашка()
    turtle.s = 1

    # Тестируем перемещения
    turtle.go_up()
    turtle.go_right()
    turtle.go_right()
    # Эволюция - увеличиваем шаг
    turtle.evolve()  # s = 2

    # Перемещаемся с новым шагом
    turtle.go_down()
    turtle.go_left()

    moves = turtle.count_moves(5, 5)

    # Пробуем деградацию
    turtle.degrade()  # s = 1

    # Пытаемся деградировать еще раз (вызовет ошибку)
    try:
        turtle.degrade()
    except ValueError as e:
        print(f"Ошибка: {e}")

    moves = turtle.count_moves(5, 5)