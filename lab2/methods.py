from dataclasses import dataclass
from math import sqrt, sin, fabs
from typing import Callable


@dataclass
class InputParameters:
    x0: float
    x1: float
    eps: float


def f(x: float):
    return 3 * x + sin(x ** 2) - 4


def df_dx(x: float, h: float) -> float | None:
    try:
        y = (f(x + h) - f(x - h)) / (2 * h)
    except TypeError:
        return
    return y


def calculate_function(params: InputParameters, func: Callable) -> tuple[list, list]:
    xlist, ylist = [], []
    x = params.x0

    while x < params.x1:
        xlist.append(x)
        x += params.eps

    for x in xlist:
        ylist.append(func(x))

    return xlist, ylist


def dichotomy_method(f: Callable, x0, x1, eps):
    if (f(x0) * f(x1)) > 0:
        return

    while fabs(x1 - x0) > eps:
        x2 = (x0 + x1) / 2

        if (f(x1) * f(x2)) <= 0:
            x0 = x2
        else:
            x1 = x2

    x = (x0 + x1) / 2
    return x


def newton_method(f: Callable, x0, eps):
    x = x0 - (f(x0) / df_dx(x0, 0.001))

    while fabs(f(x)) >= eps:
        x = x0 - (f(x0) / df_dx(x0, 0.001))
        x0 = x
    return x
