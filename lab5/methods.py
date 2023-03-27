from dataclasses import dataclass
from math import cos
from typing import Literal

import numpy as np


@dataclass
class InputParameters:
    a: float
    b: float
    N: int
    y0: float
    z0: float

    def __post_init__(self):
        self.h = (self.b - self.a) / self.N
        self.x = np.linspace(self.a, self.b, self.N)


def f(num: Literal[0] | Literal[1], x: float, u: tuple[float, float]):
    try:
        match num:
            case 0:
                return cos(u[0] + 1.1 * u[1]) + 1
            case 1:
                return (1 / (x + 2.1 * u[0] ** 2)) + x + 1
            case _:
                raise IndexError(f'В системе только {len(u)} уравнений')
    except ZeroDivisionError:
        return


def runge_kutta_2(params: InputParameters):
    y, z = [], []
    y0 = params.y0
    z0 = params.z0

    for x in params.x:
        # U_k
        u = (y0, z0)

        y.append(u[0])
        z.append(u[1])

        # U_k+1
        y0 += params.h * f(0, x + params.h / 2, (u[0] + (params.h / 2) * f(0, x, u), u[1]))
        z0 += params.h * f(1, x + params.h / 2, (u[0], u[1] + (params.h / 2) * f(1, x, u)))

    return y, z


def runge_kutta_4(params: InputParameters):
    y, z = [], []
    y0 = params.y0
    z0 = params.z0

    for x in params.x:
        # U_k
        u = (y0, z0)

        y.append(y0)
        z.append(z0)

        k1 = f(0, x, u), f(1, x, u)
        k2 = f(0, x + params.h / 2, (u[0] + k1[0] * params.h / 2, u[1])), \
            f(1, x + params.h / 2, (u[0], u[1] + k1[1] * params.h / 2))
        k3 = f(0, x + params.h / 2, (u[0] + k2[0] * params.h / 2, u[1])), \
            f(1, x + params.h / 2, (u[0], u[1] + k2[1] * params.h / 2))
        k4 = f(0, x + params.h, (u[0] + k3[0], u[1])), \
            f(1, x + params.h, (u[0], u[1] + k3[1]))


        # U_k+1
        y0 += params.h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        z0 += params.h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6

    return y, z
