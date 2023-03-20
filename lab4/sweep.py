import pytest

# region Test matrix
matrix_test = [
    [-8,       3,       0,       0,       0,       0],
    [ 5,       1,      -3,       0,       0,       0],
    [ 0,      -7,      -4,      -3,       0,       0],
    [ 0,       0,       8,       7,      -4,       0],
    [ 0,       0,       0,       1,       9,       8],
    [ 0,       0,       0,       0,       7,      -1],
]

d_test = [47, 3, -35, 4, -31, 13]
# endregion


def _calc_coeffs(matrix) -> tuple[list, list, list]:
    a, b, c = [], [], []
    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            if i == j:
                b.append(column)
            elif i == j - 1:
                c.append(column)
            elif i == j + 1:
                a.append(column)
    return a, b, c


def _calc_sweep_coeffs(i, a, b, c, d) -> tuple[float, float]:
    if i == 0:
        return -c[i] / b[i], d[i] / b[i]    # A, B
    else:
        sweep_coeffs = _calc_sweep_coeffs(i - 1, a, b, c, d)
        e = a[i-1] * sweep_coeffs[0] + b[i]
        return -c[i] / e, (d[i] - a[i-1] * sweep_coeffs[1]) / e    # A, B


def _calc_all_sweep_coeffs(a, b, c, d) -> tuple[list, list]:
    A, B = [], []

    for i in range(0, len(d) - 1):
        sweep_coeffs = _calc_sweep_coeffs(i, a, b, c, d)
        A.append(sweep_coeffs[0])
        B.append(sweep_coeffs[1])

    return A, B


def _find_roots(A, B, a, b, d) -> list:
    X = [0 for _ in range(len(d))]

    n = len(d) - 1

    X[n] = (d[n] - a[n - 1] * B[n - 1]) / (b[n] + a[n - 1] * A[n - 1])

    for i in range(n - 1, -1, -1):
        X[i] = A[i] * X[i + 1] + B[i]

    return list(map(round, X))


def sweep(matrix, d):
    # Коэффициенты перед переменными
    a, b, c = _calc_coeffs(matrix)
    print(f'a: {a}\nb: {b}\nc: {c}\n')

    # Прогоночные Коэффициенты
    A, B = _calc_all_sweep_coeffs(a, b, c, d)
    print(f'A: {A}\nB: {B}\n')

    # Корни
    X = _find_roots(A, B, a, b, d)
    print("\n".join("X{0} =\t{1:10.2f}".format(i + 1, x) for i, x in
                    enumerate(X)))

    return X


@pytest.mark.parametrize('matrix, d, x', [
    (matrix_test, d_test, [-4, 5, -6, 8, 1, -6]),
])
def test_solution(matrix, d, x):
    assert sweep(matrix, d) == x
