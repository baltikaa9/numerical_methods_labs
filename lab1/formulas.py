from math import sqrt


def f(x: float) -> float | None:
    try:
        y = (x ** 6 + 8 * x ** 3 - 128) / sqrt(8 - x ** 3)
    #        y = ((2 * x + 1) * sqrt(x * x - x)) / (x * x)
    except (ZeroDivisionError, ValueError):
        return
    return y


def df_dx_an(x: float) -> float | None:
    try:
        y = (9 * x ** 5) / (2 * sqrt(8 - x ** 3))
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
        y = (f(x) - f(x - h)) / (h)
    except TypeError:
        return
    return y


def df_dx_right(x: float, h: float) -> float | None:
    try:
        y = (f(x + h) - f(x)) / (h)
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
