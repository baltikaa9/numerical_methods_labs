from dataclasses import dataclass
from math import cos, tan, exp, cosh, sin

import numpy as np


@dataclass
class InputParameters:
    a: float
    b: float
    N: int

    def __post_init__(self):
        self.eps = (self.b - self.a) / self.N
        self.x = np.linspace(self.a, self.b, self.N)
        self.y = [f(x) for x in self.x]


def f(x: float):
    try:
        return cos(x + 1) * tan(x + 1)
        # return exp(cos(x) + 1)
        # return cosh(x)**2 + sin(x)
    except ZeroDivisionError:
        return


def golden_section_search(params: InputParameters, min: bool = True):
    # Первая лямбда, если ищем минимум, вторая - если максимум
    operation = (lambda a, b: a < b) if min else (lambda a, b: a > b)

    a = params.a
    b = params.b

    while (b - a) > params.eps:
        x1 = a + 0.381966 * (b - a)
        x2 = a + 0.618034 * (b - a)

        if operation(f(x1), f(x2)):
            b = x2
        else:
            a = x1

    return f((a + b) / 2)
