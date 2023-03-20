# --- вывод системы на экран
import pytest

# region Test matrix
matrix_test = [
    [-9,       0,       1,      -9,       1,       7],
    [ 1,      -5,       9,      -2,      -6,       8],
    [ 1,      -8,       9,      -3,       5,      -7],
    [ 2,      -3,       1,      -4,       4,      -9],
    [ 4,      -7,      -6,       2,       4,       1],
    [-2,      -0,      -4,       1,      -7,       7],
]

b_test = [
     -38,
     -14,
     196,
     128,
      62,
    -117,
]
# endregion


def fancy_print(A, B, selected):
    for row in range(len(B)):
        print("(", end='')
        for col in range(len(A[row])):
            print("\t{1:10.2f}{0}".format(" " if (selected is None
                                                  or selected != (row, col)) else "*", A[row][col]), end='')
        print("\t) * (\tX{0}) = (\t{1:10.2f})".format(row + 1, B[row]))


# --- end of вывод системы на экран

# --- перемена местами двух строк системы
def _swap_rows(A, B, row1, row2):
    A[row1], A[row2] = A[row2], A[row1]
    B[row1], B[row2] = B[row2], B[row1]


# --- end of перемена местами двух строк системы

# --- деление строки системы на число
def _divide_row(A, B, row, divider):
    A[row] = [a / divider for a in A[row]]
    B[row] /= divider


# --- end of деление строки системы на число

# --- сложение строки системы с другой строкой, умноженной на число
def _combine_rows(A, B, row, source_row, weight):
    A[row] = [(a + k * weight) for a, k in zip(A[row], A[source_row])]
    B[row] += B[source_row] * weight


# --- end of сложение строки системы с другой строкой, умноженной на число

# --- решение системы методом Гаусса (приведением к треугольному виду)
def gauss(A, B):
    column = 0
    while column < len(B):
        print("Ищем максимальный по модулю элемент в {0}-м столбце:".format(column + 1))
        current_row = None
        for row in range(column, len(A)):
            if current_row is None or abs(A[row][column]) > abs(A[current_row][column]):
                current_row = row
        if current_row is None:
            print("решений нет")
            return None
        fancy_print(A, B, (current_row, column))
        if current_row != column:
            print("Переставляем строку с найденным элементом повыше:")
            _swap_rows(A, B, current_row, column)
            fancy_print(A, B, (column, column))
        print("Нормализуем строку с найденным элементом:")
        _divide_row(A, B, column, A[column][column])
        fancy_print(A, B, (column, column))
        print("Обрабатываем нижележащие строки:")
        for row in range(column + 1, len(A)):
            _combine_rows(A, B, row, column, -A[row][column])
        fancy_print(A, B, (column, column))
        column += 1
    print("Матрица приведена к треугольному виду, считаем решение")
    X = [0 for _ in B]
    for i in range(len(B) - 1, -1, -1):
        X[i] = B[i] - sum(x * a for x, a in zip(X[(i + 1):], A[i][(i + 1):]))
    print("Получили ответ:")
    print("\n".join("X{0} =\t{1:10.2f}".format(i + 1, x) for i, x in
                    enumerate(X)))

    X = list(map(round, X))
    return X
# --- end of решение системы методом Гаусса (приведением к треугольному виду)


@pytest.mark.parametrize('matrix, d, x', [
    (matrix_test, b_test, [1, -9, 4, -1, 7, -7]),
])
def test_solution(matrix, d, x):
    assert gauss(matrix, d) == x
