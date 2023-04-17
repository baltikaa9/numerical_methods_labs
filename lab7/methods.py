from dataclasses import dataclass
from math import cos, tan, exp, cosh, sin, sqrt

import numpy as np


@dataclass
class InputParameters:
    a: float
    b: float
    N: int

    def __post_init__(self):
        self.eps = (self.b - self.a) / self.N
        self.x = np.linspace(self.a, self.b, self.N)
        self.y = np.linspace(self.a, self.b, self.N)
        self.z = [[F(x, y) for x in self.x] for y in self.y]


def F(x, y):
    return (-1 - 2 * y**2 - x)**2 + (y - (3 - x) / 2)**2
    # return (cos(y) - x)**2 + (2 * sin(y) - 6 / (x**3 + 2))**2
    # return x**2 + y**2
    # return (2*y**2 - 2*y + 4)**2


def dFdx(x, y):
    return 5 * x / 2 + 4 * y**2 + y + 0.5
    # return 2 * ((36 * x**2 * ((x**3 + 2) * sin(y) - 3)) / ((x**3 + 2)**3) + x - sin(y))
    # return 2 * x
    # return 0


def dFdy(x, y):
    return 8 * x * y + x + 16 * y**3 + 10 * y - 3
    # return 2 * cos(y) * (-12 / (x**3 + 2) - x + 5 * sin(y))
    # return 2 * y
    # return 8*(2*y-1)*(y**2-y+2)


def gradient_descent(graph=None):
    t = 0.05
    x = 0
    y = 0
    for n in range(50):
        gradx = (dFdx(x, y))
        grady = (dFdy(x, y))
        gradx, grady = map(np.sign, (gradx, grady))
        x -= t * gradx
        y -= t * grady
        if graph is not None:
            graph.draw_scatter(x, y, F(x, y), color='r')
        print(x, y, F(x, y))
    return x, y


if __name__ == '__main__':
    x, y = gradient_descent()
    print(x, (3-x)/2, sqrt(F(x, y)))
    print(-1-2*y**2, y, sqrt(F(x, y)))
