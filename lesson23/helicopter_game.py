import random
import time
import os
import json
from enum import Enum
from collections import deque


class CellType(Enum):
    EMPTY = " "
    TREE = "🌲"
    RIVER = "🌊"
    FIRE = "🔥"
    BURNED = "⚫"
    HELICOPTER = "🚁"


class HelicopterGame:
    def __init__(self, width=15, height=10):
        # Игровое поле
        self.width = width
        self.height = height
        self.grid = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]

        # Позиция вертолета
        self.helicopter_x = width // 2
        self.helicopter_y = height // 2

        # Статистика игры
        self.helicopter_water = 0
        self.helicopter_max_water = 3
        self.score = 0
        self.lives = 3
        self.money = 0
        self.tick_count = 0

        # История сообщений (последние 5 сообщений)
        self.message_history = deque(maxlen=5)
        self.add_message("🚁 Игра началась! Добро пожаловать!")

        # Генерация карты
        self.generate_rivers()
        self.generate_trees()

    def add_message(self, message):
        """Добавляет сообщение в историю"""
        self.message_history.append(f"[Ход {self.tick_count}] {message}")

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def generate_rivers(self, num_rivers=None):
        if num_rivers is None:
            # Автоматически рассчитываем количество рек в зависимости от размера карты
            num_rivers = max(2, min(5, self.width * self.height // 50))

        for _ in range(num_rivers):
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)

            x, y = start_x, start_y
            river_length = random.randint(
                max(3, self.width // 3),
                max(5, self.width // 2)
            )

            for _ in range(river_length):
                if self.is_within_bounds(x, y):
                    self.grid[y][x] = CellType.RIVER
                direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                x += direction[0]
                y += direction[1]

    def generate_trees(self, tree_density=None):
        if tree_density is None:
            # Автоматическая плотность деревьев в зависимости от размера карты
            tree_density = 0.4

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == CellType.EMPTY and random.random() < tree_density:
                    self.grid[y][x] = CellType.TREE

    def get_random_cell(self, cell_type=None, max_attempts=100):
        """
        Получение случайной клетки определенного типа
        max_attempts - максимальное количество попыток для избежания бесконечного цикла
        """
        attempts = 0
        while attempts < max_attempts:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if cell_type is None or self.grid[y][x] == cell_type:
                return x, y
            attempts += 1

        # Если не нашли нужный тип за max_attempts попыток, возвращаем любую клетку
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        return x, y

    def count_cells_of_type(self, cell_type):
        """Подсчитывает количество клеток определенного типа"""
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == cell_type:
                    count += 1
        return count

    def generate_fire(self):
        # Проверяем, есть ли вообще деревья для поджигания
        tree_count = self.count_cells_of_type(CellType.TREE)
        if tree_count == 0:
            return

        # Вероятность пожара зависит от размера карты
        fire_chance = 0.2
        if self.width * self.height > 300:  # Большие карты
            fire_chance = 0.15
        elif self.width * self.height < 100:  # Маленькие карты
            fire_chance = 0.3

        if random.random() < fire_chance:
            x, y = self.get_random_cell(CellType.TREE)
            if self.grid[y][x] == CellType.TREE:  # Двойная проверка
                self.grid[y][x] = CellType.FIRE
                self.add_message("🔥 Появился новый пожар!")

    def spread_fire(self):
        new_fires = []
        fire_count = self.count_cells_of_type(CellType.FIRE)

        if fire_count == 0:
            return

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == CellType.FIRE:
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = x + dx, y + dy
                        if (self.is_within_bounds(nx, ny) and
                                self.grid[ny][nx] == CellType.TREE and
                                random.random() < 0.4):
                            new_fires.append((nx, ny))

        for x, y in new_fires:
            self.grid[y][x] = CellType.FIRE

        if new_fires:
            self.add_message(f"🔥 Огонь распространился на {len(new_fires)} новых деревьев!")

    def update_fire(self):
        """Обновление состояния пожаров - сгоревшие деревья превращаются в пепел"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == CellType.FIRE:
                    if random.random() < 0.1:
                        self.grid[y][x] = CellType.BURNED
                        self.score -= 5
                        self.add_message("💀 Дерево сгорело! -5 очков")

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        print("=" * 60)
        print(f"🚁 ВЕРТОЛЕТ-ПОЖАРНЫЙ | Карта: {self.width}x{self.height}")
        print("=" * 60)

        # Отрисовка карты
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if x == self.helicopter_x and y == self.helicopter_y:
                    row += CellType.HELICOPTER.value + " "
                else:
                    row += self.grid[y][x].value + " "
            print(row)

        # Статистика по клеткам
        tree_count = self.count_cells_of_type(CellType.TREE)
        fire_count = self.count_cells_of_type(CellType.FIRE)
        river_count = self.count_cells_of_type(CellType.RIVER)
        burned_count = self.count_cells_of_type(CellType.BURNED)

        # Статус
        print("\n" + "=" * 60)
        print(
            f"💧 Вода: {self.helicopter_water}/{self.helicopter_max_water} | ⭐ Очки: {self.score} | ❤️  Жизни: {self.lives}")
        print(f"💰 Деньги: {self.money} | ⏰ Ход: {self.tick_count}")
        print(f"🌲 Деревья: {tree_count} | 🔥 Пожары: {fire_count} | 🌊 Реки: {river_count} | ⚫ Пепел: {burned_count}")
        print("=" * 60)

        # История сообщений
        print("\n📜 ПОСЛЕДНИЕ СОБЫТИЯ:")
        if self.message_history:
            for msg in reversed(self.message_history):  # Показываем новые сверху
                print(f"  {msg}")
        else:
            print("  Пока ничего не произошло...")

        print("=" * 60)
        print("Управление: WASD - движение, E - тушение пожаров вокруг")
        print("Q - выход, S - сохранить, L - загрузить, M - магазин")
        print("R - случайная телепортация, HELP - справка")

    def extinguish_fires_around(self):
        """Тушит пожары в радиусе одной клетки вокруг вертолета"""
        if self.helicopter_water <= 0:
            self.add_message("❌ Нет воды для тушения!")
            print("❌ Нет воды для тушения!")
            return

        fires_extinguished = 0
        saved_trees = 0
        # Проверяем все клетки вокруг вертолета (включая диагонали)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Пропускаем саму клетку с вертолетом
                if dx == 0 and dy == 0:
                    continue

                nx = self.helicopter_x + dx
                ny = self.helicopter_y + dy

                if self.is_within_bounds(nx, ny):
                    if self.grid[ny][nx] == CellType.FIRE:
                        # Возвращаем дерево вместо удаления!
                        self.grid[ny][nx] = CellType.TREE
                        fires_extinguished += 1
                        saved_trees += 1

        if fires_extinguished > 0:
            self.helicopter_water -= 1
            points_earned = fires_extinguished * 20
            money_earned = fires_extinguished * 5
            self.score += points_earned
            self.money += money_earned

            self.add_message(
                f"✅ Потушено {fires_extinguished} пожаров! Спасено {saved_trees} деревьев! +{points_earned} очков, +{money_earned} денег")
            print(
                f"✅ Потушено {fires_extinguished} пожаров! Спасено {saved_trees} деревьев! +{points_earned} очков, +{money_earned} денег")
        else:
            self.add_message("ℹ️  Пожаров для тушения рядом нет")
            print("ℹ️  Пожаров для тушения рядом нет")

    def helicopter_interact(self):
        """Основное взаимодействие вертолета с окружением"""
        cell_type = self.grid[self.helicopter_y][self.helicopter_x]

        # Набор воды из реки
        if cell_type == CellType.RIVER and self.helicopter_water < self.helicopter_max_water:
            self.helicopter_water = self.helicopter_max_water
            self.add_message("💧 Вода набрана из реки!")
            print("💧 Вода набрана из реки!")

        # Тушение пожаров вокруг
        elif self.helicopter_water > 0:
            self.extinguish_fires_around()
        else:
            self.add_message("ℹ️  Здесь не с чем взаимодействовать")

    def move_helicopter(self, dx, dy):
        new_x = self.helicopter_x + dx
        new_y = self.helicopter_y + dy

        if self.is_within_bounds(new_x, new_y):
            self.helicopter_x = new_x
            self.helicopter_y = new_y

            # Проверяем, не в огне ли вертолет
            if self.grid[self.helicopter_y][self.helicopter_x] == CellType.FIRE:
                self.lives -= 1
                self.add_message("💥 Вертолет в огне! -1 жизнь")
                print("💥 Вертолет в огне! -1 жизнь")
                if self.lives <= 0:
                    self.add_message("💀 Игра окончена!")
                    print("💀 Игра окончена!")
                    return False

        return True

    def random_teleport(self):
        """Телепортирует вертолет в случайную позицию"""
        self.helicopter_x = random.randint(0, self.width - 1)
        self.helicopter_y = random.randint(0, self.height - 1)
        self.add_message(f"🎯 Телепортация в позицию ({self.helicopter_x}, {self.helicopter_y})")
        print(f"🎯 Телепортация в позицию ({self.helicopter_x}, {self.helicopter_y})")

        # Проверяем, не телепортировались ли в огонь
        if self.grid[self.helicopter_y][self.helicopter_x] == CellType.FIRE:
            self.lives -= 1
            self.add_message("💥 Телепортация в огонь! -1 жизнь")
            print("💥 Телепортация в огонь! -1 жизнь")
            if self.lives <= 0:
                self.add_message("💀 Игра окончена!")
                print("💀 Игра окончена!")
                return False

        return True

    def show_shop(self):
        """Показывает магазин улучшений"""
        print("\n" + "=" * 40)
        print("🏪 МАГАЗИН УЛУЧШЕНИЙ")
        print("=" * 40)
        print(f"1. 📦 Увеличить емкость воды (+1) - 50 денег (текущая: {self.helicopter_max_water})")
        print(f"2. 💖 Купить жизнь (+1) - 100 денег (текущие: {self.lives})")
        print(f"3. 💰 Обменять 50 очков на 20 денег")
        print("4. 🌲 Посадить дерево (10 денег)")
        print("5. 🔥 Восстановить сгоревшее дерево (15 денег)")
        print("6. ❌ Выйти из магазина")
        print("=" * 40)

        choice = input("Выберите улучшение (1-6): ").strip().lower()

        if choice == '1':
            if self.money >= 50:
                self.helicopter_max_water += 1
                self.money -= 50
                self.add_message("✅ Емкость воды увеличена!")
                print("✅ Емкость воды увеличена!")
            else:
                print("❌ Недостаточно денег! Нужно 50.")

        elif choice == '2':
            if self.money >= 100:
                self.lives += 1
                self.money -= 100
                self.add_message("✅ +1 жизнь!")
                print("✅ +1 жизнь!")
            else:
                print("❌ Недостаточно денег! Нужно 100.")

        elif choice == '3':
            if self.score >= 50:
                self.score -= 50
                self.money += 20
                self.add_message("✅ Обмен выполнен: 50 очков → 20 денег")
                print("✅ Обмен выполнен: 50 очков → 20 денег")
            else:
                print("❌ Недостаточно очков! Нужно 50.")

        elif choice == '4':
            if self.money >= 10:
                # Ищем пустую клетку для посадки дерева
                x, y = self.get_random_cell(CellType.EMPTY)
                if self.grid[y][x] == CellType.EMPTY:
                    self.grid[y][x] = CellType.TREE
                    self.money -= 10
                    self.add_message(f"✅ Дерево посажено в позиции ({x}, {y})!")
                    print(f"✅ Дерево посажено в позиции ({x}, {y})!")
                else:
                    print("❌ Не удалось найти место для дерева")
            else:
                print("❌ Недостаточно денег! Нужно 10.")

        elif choice == '5':
            if self.money >= 15:
                # Ищем сгоревшее дерево для восстановления
                x, y = self.get_random_cell(CellType.BURNED)
                if self.grid[y][x] == CellType.BURNED:
                    self.grid[y][x] = CellType.TREE
                    self.money -= 15
                    self.add_message(f"✅ Восстановлено сгоревшее дерево в позиции ({x}, {y})!")
                    print(f"✅ Восстановлено сгоревшее дерево в позиции ({x}, {y})!")
                else:
                    print("❌ Нет сгоревших деревьев для восстановления")
            else:
                print("❌ Недостаточно денег! Нужно 15.")

        elif choice == '6':
            print("Выход из магазина...")

        else:
            print("❌ Неверный выбор!")

    def game_tick(self):
        self.tick_count += 1

        # Генерация новых пожаров
        self.generate_fire()

        # Распространение существующих пожаров
        self.spread_fire()

        # Обновление состояния пожаров
        self.update_fire()

        # Случайная гроза (только если есть пожары)
        fire_count = self.count_cells_of_type(CellType.FIRE)
        if fire_count > 0 and random.random() < 0.1:
            fires_extinguished = 0
            trees_saved = 0
            max_attempts = min(3, fire_count)  # Не больше попыток чем пожаров

            for _ in range(max_attempts):
                x, y = self.get_random_cell(CellType.FIRE)
                if self.grid[y][x] == CellType.FIRE:
                    self.grid[y][x] = CellType.TREE  # Гроза тоже спасает деревья!
                    fires_extinguished += 1
                    trees_saved += 1

            if fires_extinguished > 0:
                self.add_message(f"⛈️  Гроза потушила {fires_extinguished} пожаров и спасла {trees_saved} деревьев!")

    def save_game(self, filename="helicopter_save.json"):
        save_data = {
            "width": self.width,
            "height": self.height,
            "grid": [[cell.value for cell in row] for row in self.grid],
            "helicopter": {"x": self.helicopter_x, "y": self.helicopter_y, "water": self.helicopter_water},
            "stats": {
                "score": self.score,
                "lives": self.lives,
                "money": self.money,
                "tick_count": self.tick_count,
                "max_water": self.helicopter_max_water
            },
            "messages": list(self.message_history)
        }

        with open(filename, 'w') as f:
            json.dump(save_data, f)
        self.add_message(f"💾 Игра сохранена в {filename}")
        print(f"💾 Игра сохранена в {filename}")

    def load_game(self, filename="helicopter_save.json"):
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)

            # Восстанавливаем размеры карты
            self.width = save_data.get("width", 15)
            self.height = save_data.get("height", 10)

            # Создаем новую сетку
            self.grid = [[CellType.EMPTY for _ in range(self.width)] for _ in range(self.height)]

            # Восстанавливаем enum значения
            cell_mapping = {v: CellType(v) for v in [ct.value for ct in CellType]}
            loaded_grid = save_data["grid"]

            # Загружаем сохраненную карту
            for y in range(min(self.height, len(loaded_grid))):
                for x in range(min(self.width, len(loaded_grid[y]))):
                    self.grid[y][x] = cell_mapping[loaded_grid[y][x]]

            heli = save_data["helicopter"]
            self.helicopter_x = min(heli["x"], self.width - 1)
            self.helicopter_y = min(heli["y"], self.height - 1)
            self.helicopter_water = heli["water"]

            stats = save_data["stats"]
            self.score = stats["score"]
            self.lives = stats["lives"]
            self.money = stats["money"]
            self.tick_count = stats["tick_count"]
            self.helicopter_max_water = stats.get("max_water", 3)

            # Восстанавливаем историю сообщений
            if "messages" in save_data:
                self.message_history = deque(save_data["messages"], maxlen=5)

            self.add_message(f"📂 Игра загружена из {filename}")
            print(f"📂 Игра загружена из {filename}")

        except FileNotFoundError:
            print("❌ Файл сохранения не найден")
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")

    def process_command(self, command):
        """Обрабатывает команду без учета регистра"""
        command = command.strip().lower()

        if command in ['w', 'в']:  # русская и английская w
            return self.move_helicopter(0, -1)
        elif command in ['s', 'ы']:  # русская и английская s
            return self.move_helicopter(0, 1)
        elif command in ['a', 'ф']:  # русская и английская a
            return self.move_helicopter(-1, 0)
        elif command in ['d', 'в']:  # русская и английская d
            return self.move_helicopter(1, 0)
        elif command in ['e', 'у']:  # русская и английская e
            self.helicopter_interact()
            return True
        elif command in ['s', 'ы', 'save', 'сохранить']:
            self.save_game()
            return True
        elif command in ['l', 'д', 'load', 'загрузить']:
            self.load_game()
            return True
        elif command in ['m', 'ь', 'shop', 'магазин']:
            self.show_shop()
            return True
        elif command in ['r', 'к', 'random', 'телепорт']:
            return self.random_teleport()
        elif command in ['q', 'й', 'quit', 'выход']:
            print("👋 До свидания!")
            return False
        elif command in ['help', 'помощь', '?']:
            self.show_help()
            return True
        elif command in ['clear', 'очистить']:
            self.message_history.clear()
            self.add_message("📜 История сообщений очищена")
            print("📜 История сообщений очищена")
            return True
        else:
            self.add_message("❌ Неизвестная команда")
            print("❌ Неизвестная команда. Введите 'help' для справки.")
            return True

    def show_help(self):
        """Показывает справку по командам"""
        print("\n" + "=" * 50)
        print("📖 СПРАВКА ПО КОМАНДАМ")
        print("=" * 50)
        print("W или В - Движение вверх")
        print("S или Ы - Движение вниз")
        print("A или Ф - Движение влево")
        print("D или В - Движение вправо")
        print("E или У - Тушение пожаров вокруг вертолета")
        print("R или К - Случайная телепортация")
        print("S или SAVE - Сохранить игру")
        print("L или LOAD - Загрузить игру")
        print("M или SHOP - Магазин улучшений")
        print("Q или QUIT - Выход из игры")
        print("CLEAR - Очистить историю сообщений")
        print("HELP - Эта справка")
        print("")
        print("🔥 ТУШЕНИЕ ПОЖАРОВ:")
        print("  - Используйте E для тушения пожаров вокруг")
        print("  - Тушатся все пожары в радиусе 1 клетки")
        print("  - 1 единица воды = все пожары вокруг")
        print("  - Потушили вовремя? Дерево сохраняется! 🌲")
        print("  - +20 очков и +5 денег за каждый потушенный пожар")
        print("")
        print("💀 СГОРЕВШИЕ ДЕРЕВЬЯ:")
        print("  - Если не успели потушить, дерево сгорает ⚫")
        print("  - Сгоревшие деревья можно восстановить в магазине")
        print("=" * 50)
        input("Нажмите Enter чтобы продолжить...")

    def run(self):
        print("🚁 Добро пожаловать в игру 'Вертолет-пожарный'!")
        print("Тушите пожары (🔥) вокруг вертолета, набирайте воду из рек (🌊)")
        print("Спасайте деревья от огня! Введите 'help' для просмотра всех команд")

        running = True
        while running and self.lives > 0:
            self.draw()
            self.game_tick()

            command = input("\nВведите команду: ")
            running = self.process_command(command)

        if self.lives <= 0:
            print("💀 Игра окончена! Вы проиграли.")
            print(f"🏆 Ваш финальный счет: {self.score}")


def get_map_size():
    """Функция для выбора размера карты"""
    print("\n" + "=" * 50)
    print("🎯 ВЫБОР РАЗМЕРА КАРТЫ")
    print("=" * 50)
    print("1. 🔸 Маленькая (10x8) - для начинающих")
    print("2. 🔹 Средняя (15x10) - стандартный размер")
    print("3. 🔸 Большая (20x15) - для опытных игроков")
    print("4. 🔹 Огромная (25x18) - настоящий вызов!")
    print("5. 🔸 Свой размер - введите ширину и высоту")
    print("=" * 50)

    while True:
        choice = input("Выберите размер карты (1-5): ").strip()

        if choice == '1':
            return 10, 8
        elif choice == '2':
            return 15, 10
        elif choice == '3':
            return 20, 15
        elif choice == '4':
            return 25, 18
        elif choice == '5':
            try:
                width = int(input("Введите ширину карты (5-30): "))
                height = int(input("Введите высоту карты (5-20): "))
                if 5 <= width <= 30 and 5 <= height <= 20:
                    return width, height
                else:
                    print("❌ Неверный размер! Ширина: 5-30, Высота: 5-20")
            except ValueError:
                print("❌ Введите числа!")
        else:
            print("❌ Неверный выбор! Введите число от 1 до 5")


# Запуск игры
if __name__ == "__main__":
    print("🚁 ВЕРТОЛЕТ-ПОЖАРНЫЙ")
    print("=" * 50)

    # Выбор размера карты
    width, height = get_map_size()

    # Создание и запуск игры
    game = HelicopterGame(width, height)
    game.run()