from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class InputParameters:
    x0: float
    x1: float
    y0: float
    y1: float
    N: int = 1000

    def __post_init__(self):
        self.h = (self.x1 - self.x0) / self.N
        self.x = np.linspace(self.x0, self.x1, self.N)


def system(x: float, u: tuple[float, float]):
    """
    u[0] = y
    u[1] = z
    """
    return u[1], u[0] + 2 * x


def runge_kutta(system: Callable, interval, u0):
    y, z = [], []
    y0 = u0[0]
    z0 = u0[1]
    N = 1000
    h = (interval[1] - interval[0]) / N

    _x = np.linspace(interval[0], interval[1], N)

    for x in _x:
        # U_k
        u = (y0, z0)

        y.append(y0)
        z.append(z0)

        k1 = system(x, u)[0], system(x, u)[1]
        k2 = system(x + h / 2, (u[0] + k1[0] * h / 2, u[1]))[0], \
            system(x + h / 2, (u[0], u[1] + k1[1] * h / 2))[1]
        k3 = system(x + h / 2, (u[0] + k2[0] * h / 2, u[1]))[0], \
            system(x + h / 2, (u[0], u[1] + k2[1] * h / 2))[1]
        k4 = system(x + h, (u[0] + k3[0], u[1]))[0], \
            system(x + h, (u[0], u[1] + k3[1]))[1]

        # U_k+1
        y0 += h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        z0 += h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6

    return y, z


def dichotomy(f: Callable, x0, x1, eps, params: InputParameters):
    if (f(x0, params) * f(x1, params)) > 0:
        return

    while abs(x1 - x0) > eps:
        x2 = (x0 + x1) / 2

        if f(x2, params) > params.y1:
            x1 = x2
        else:
            x0 = x2

    x = (x0 + x1) / 2
    return x


def shoot(a, params: InputParameters):
    y0 = (params.y0, a)

    sol = runge_kutta(system, [params.x0, params.x1], y0)
    y1 = sol[0][-1]
    return y1


def shooting_method(params: InputParameters):
    a0 = -100
    a1 = 100

    a = dichotomy(shoot, a0, a1, 1e-6, params)

    if a is None:
        a0 = -10000
        a1 = 10000
        a = dichotomy(shoot, a0, a1, 1e-6, params)

    try:
        y = runge_kutta(system, [params.x0, params.x1], [params.y0, a])
    except TypeError:
        raise ValueError('Неадекватные начальные условия')

    return y[0]


if __name__ == '__main__':
    params = InputParameters(0, 1, 0, -1)
    print(params.x, shooting_method(params))
