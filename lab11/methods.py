from dataclasses import dataclass
from math import cos, sin, sqrt
from typing import Callable

import numpy as np


@dataclass
class InputParameters:
    x0: float
    x1: float
    m: int

    def __post_init__(self):
        self.n = 2 * self.m + 1
        self.x = np.linspace(self.x0, self.x1, self.n)
        self.y = [x+1 for x in self.x]
        self.T = 2 * np.pi
        self.freq = (2 * np.pi) / self.T


def furier_series(x, a, b, freq, m):
    sum = 0
    for k in range(1, m + 1):
        sum += (a[k] * cos(k * freq * x) + b[k] * sin(k * freq * x))
    return (a[0] / 2) + sum


def furier_coeffs(x, y, freq, m):
    a, b = [], [0]
    for k in range(m + 1):
        a.append(_a(x, y, k, freq))

    for k in range(1, m + 1):
        b.append(_b(x, y, k, freq))
    return a, b


def _a(x, y, k, freq):
    sum = 0
    for i in range(len(x)):
        sum += y[i] * cos(k * freq * x[i])
    return (2 / len(x)) * sum
    # h = x[1] - x[0]
    # sum = 0
    # for i in range(len(x)):
    #     sum += y[i] * cos(k * x[i])
    # return sum * h * (1 / np.pi)


def _b(x, y, k, freq):
    sum = 0
    for i in range(len(x)):
        sum += y[i] * sin(k * freq * x[i])
    return (2 / len(x)) * sum
    # h = x[1] - x[0]
    # sum = 0
    # for i in range(len(x)):
    #     sum += y[i] * sin(k * x[i])
    # return sum * h * (1 / np.pi)


def dispersion(y, f):
    sum = 0
    for i in range(len(y)):
        sum += (y[i] - f[i])**2
    sum *= (1 / len(y))
    return sqrt(sum)


if __name__ == '__main__':
    params = InputParameters(0, 1, 11, 3)
    a, b = furier_coeffs(params.x, params.y, params.freq, params.m)
    print(furier_series(0.5, a, b, params.freq, params.m))
