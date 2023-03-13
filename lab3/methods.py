from dataclasses import dataclass
from typing import Callable


@dataclass
class InputParameters:
    a: float
    b: float
    N: float

    def __post_init__(self):
        self.h = (self.b - self.a) / self.N


def f(x: float):
    try:
        return x ** 3 / (1 + x)
    except ZeroDivisionError:
        return


def df_dx(x: float, h: float) -> float | None:
    try:
        y = (f(x + h) - f(x - h)) / (2 * h)
    except TypeError:
        return
    return y


def calculate_function(params: InputParameters, func: Callable) -> tuple[list, list]:
    xlist, ylist = [], []
    x = params.a

    while x <= params.b:
        xlist.append(x)
        x += params.h

    for x in xlist:
        ylist.append(func(x))

    return xlist, ylist


def rectangle_method(params: InputParameters):
    x = params.a
    sum = 0
    while x <= params.b:
        if (y := f(x)) is not None: sum += y
        x += params.h
    return sum * params.h


def trapezoid_formula(params: InputParameters):
    x = params.a
    sum = 0

    if (y := f(x)) is not None: sum += y
    x += params.h

    while x < params.b:
        if (y := 2 * f(x)) is not None: sum += y
        x += params.h

    if (y := f(x)) is not None: sum += y
    return sum * (params.b - params.a) / (2 * params.N)


def simpson_formula(params: InputParameters):
    x = params.a
    sum = 0
    i = 1

    if (y := f(x)) is not None: sum += y
    x += params.h

    while x < params.b:
        if i % 2:
            if (y := 4 * f(x)) is not None: sum += y
        else:
            if (y := 2 * f(x)) is not None: sum += y
        x += params.h
        i += 1

    if (y := f(x)) is not None: sum += y
    return sum * (params.b - params.a) / (3 * params.N)
