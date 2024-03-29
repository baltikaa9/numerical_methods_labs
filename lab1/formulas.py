from dataclasses import dataclass
from math import sqrt
from typing import Callable


@dataclass
class InputParameters:
    a: float
    b: float
    N: int

    def __post_init__(self):
        self.h = (self.b - self.a) / self.N


def f(x: float) -> float | None:
    try:
        y = (x ** 6 + 8 * x ** 3 - 128) / sqrt(8 - x ** 3)
        # y = ((1 + x**8) * sqrt(1 + x**8)) / (12 * x**12)
        # y = ((2 * x + 1) * sqrt(x * x - x)) / (x * x)
        # y = (2*x**2-x-1) / (3 * sqrt(2+4*x))
    except (ZeroDivisionError, ValueError):
        return
    return y


def df_dx_an(x: float) -> float | None:
    try:
        y = (9 * x ** 5) / (2 * sqrt(8 - x ** 3))
        # y = - sqrt(x**8 + 1) / x**13
    except (ZeroDivisionError, ValueError):
        return
    return y


def df_dx(x: float, h: float) -> float | None:
    try:
        y = (f(x + h) - f(x - h)) / (2 * h)
    except TypeError:
        return
    return y


def df_dx_left(x: float, h: float) -> float | None:
    try:
        y = (f(x) - f(x - h)) / h
    except TypeError:
        return
    return y


def df_dx_right(x: float, h: float) -> float | None:
    try:
        y = (f(x + h) - f(x)) / h
    except TypeError:
        return
    return y


def d2f_dx2(x: float, h: float) -> float | None:
    try:
        y = (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)
    except TypeError:
        return
    return y


def d2f_dx2_an(x: float) -> float | None:
    try:
        y = (9 * x ** 4 * (80 - 7 * x ** 3)) / (4 * sqrt(8 - x ** 3) ** 3)
    except (ZeroDivisionError, ValueError):
        return
    return y


def d3f_dx3(x: float, h: float) -> float | None:
    try:
        y = (f(x + 2 * h) - 2 * f(x + h) + 2 * f(x - h) - f(x - 2 * h)) / (2 * h * h * h)
    except TypeError:
        return
    return y


def d3f_dx3_an(x: float) -> float | None:
    try:

        y = (9 * x ** 3 * (35 * x ** 6 - 704 * x ** 3 + 5120)) / (8 * sqrt(8 - x ** 3) ** 5)
    except (ZeroDivisionError, ValueError):
        return
    return y


def calculate_derivative(params: InputParameters, func: Callable) -> tuple[list, list]:
    xlist, ylist = [], []
    x = params.a

    while x < params.b:
        xlist.append(x)
        x += params.h

    for x in xlist:
        try:
            ylist.append(func(x, params.h))
        except TypeError:
            ylist.append(func(x))

    return xlist, ylist
