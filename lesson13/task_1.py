import random


def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Ошибка: размер матрицы должен быть положительным числом!")
                continue
            return value
        except ValueError:
            print("Ошибка: введите целое число!")


def generate_matrix(rows, cols, min_value=0, max_value=10):
    return [[random.randint(min_value, max_value) for _ in range(cols)] for _ in range(rows)]


def print_matrix(matrix, name):
    """Вывод матрицы в консоль с названием"""
    print(f"\n{name}:")
    for row in matrix:
        print(row)


def add_matrices(matrix1, matrix2):
    """Сложение двух матриц"""
    rows = len(matrix1)
    cols = len(matrix1[0])

    result = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(matrix1[i][j] + matrix2[i][j])
        result.append(row)

    return result


def main():
    print("=== ГЕНЕРАТОР И СУММАТОР МАТРИЦ ===")

    # Получаем размеры матриц от пользователя
    rows = get_positive_integer("Введите количество строк матриц: ")
    cols = get_positive_integer("Введите количество столбцов матриц: ")

    # Генерируем матрицы
    print(f"\nГенерация матриц размером {rows}x{cols}...")
    matrix_1 = generate_matrix(rows, cols)
    matrix_2 = generate_matrix(rows, cols)

    # Выводим исходные матрицы
    print_matrix(matrix_1, "Матрица 1")
    print_matrix(matrix_2, "Матрица 2")

    # Складываем матрицы
    matrix_3 = add_matrices(matrix_1, matrix_2)

    # Выводим результат
    print_matrix(matrix_3, "Матрица 3 (Сумма матриц 1 и 2)")

    print("\nОперация завершена успешно!")


if __name__ == "__main__":
    main()