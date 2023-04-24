from dataclasses import dataclass
from math import exp

import numpy as np

from lab4.sweep import sweep


@dataclass
class InputParameters:
    a: int = -1
    b: int = 0
    n: int = 4

    def __post_init__(self):
        self.N = self.n - 1
        self.f = lambda x: 5 * x ** 5 + 3 * x ** 3 - 4 * x ** 2 - 9 * x + 100
        # self.f = lambda x: exp(-x**2 + 10*x - 4.2)

        self.x = np.linspace(self.a, self.b, self.n)
        self.y = [self.f(x) for x in self.x]
        # self.y = [1.0002, 1.0341, 0.6, 0.40105, 0.1, 0.23975]
        self.h = [None if i == 0 else self.x[i] - self.x[i-1] for i in range(self.N+1)]


@dataclass
class Spline:
    a: float
    b: float
    c: float
    d: float
    x: float


# Построение сплайна
# x - узлы сетки, должны быть упорядочены по возрастанию, кратные узлы запрещены
# y - значения функции в узлах сетки
# n - количество узлов сетки
def build_splines(x, y, n, params: InputParameters):
    # Инициализация массива сплайнов
    splines = [Spline(0, 0, 0, 0, 0) for _ in range(0, n)]
    for i in range(1, n):
        splines[i].x = x[i-1]
        splines[i].a = y[i-1]

    A = _matrix_a(params.n, params.h)
    B = _matrix_b(params.n, params.h, params.y)

    c = [0, 0] + sweep(A, B) + [0]
    for i, spline in enumerate(splines):
        spline.c = c[i]

    for i in range(1, params.n):
        splines[i].d = (c[i+1] - c[i]) / (3 * params.h[i])
        splines[i].b = (params.y[i] - splines[i].a - splines[i].c * params.h[i]**2 - splines[i].d * params.h[i]**3) / params.h[i]
    return splines[1:]


def _matrix_a(n: int, h: list):
    A = [[0 for _ in range(n-2)] for _ in range(n-2)]
    A[0][0] = 2 * (h[1] + h[2])
    A[0][1] = h[2]
    A[n-3][n-4] = h[n-2]
    A[n-3][n-3] = 2 * (h[n-2] + h[n-1])

    for i in range(1, n-3):
        for j in range(n-2):
            if i - j == 1:
                A[i][j] = h[i+1]
            elif i == j:
                A[i][j] = 2 * (h[j] + h[j+1])
            elif j - i == 1:
                A[i][j] = h[j+1]
    return A


def _matrix_b(n: int, h: list, y: list):
    return [3 * ((y[i+2] - y[i+1]) / h[i+2] - (y[i+1] - y[i]) / h[i+1]) for i in range(n-2)]


# Вычисление значения интерполированной функции в произвольной точке
def interpolate(splines, x):
    if not splines:
        return None  # Если сплайны ещё не построены - возвращаем NaN

    n = len(splines)

    if x <= splines[0].x:  # Если x меньше точки сетки x[0] - пользуемся первым эл-тов массива
        s = splines[0]
    elif x >= splines[n - 1].x:  # Если x больше точки сетки x[n - 1] - пользуемся последним эл-том массива
        s = splines[n - 1]
    else:  # Иначе x лежит между граничными точками сетки - производим бинарный поиск нужного эл-та массива
        i = 0
        j = n - 1
        while i + 1 < j:
            k = i + (j - i) // 2
            if x <= splines[k].x:
                j = k
            else:
                i = k
        s = splines[j-1]

    dx = x - s.x
    return s.a + s.b * dx + s.c * dx ** 2 + s.d * dx ** 3
