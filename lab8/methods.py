from dataclasses import dataclass
from math import cos, tan, exp, cosh, sin, sqrt, log

import numpy as np


@dataclass
class InputParameters:
    n: int = 20  # кол-во измерений
    p: int = 3  # кол-во коэфф-тов а

    def __post_init__(self):
        self.x = np.array([x + 1 for x in range(self.n)])
        self.y = np.array([-2.28, -2.83, -1.45, -1.40, -2.33, 0.09, -1.96, -2.28, -0.36, 0.71,
                           -0.80, 0.26, -0.06, -0.29, 1.26, 0.68, 0.19, 1.04, 0.60, 1.94])

        # self.x = [round(x, 1) for x in list(np.arange(0, 1, 0.1)) + list(np.arange(1.1, 2.1, 0.1))]
        # self.y = np.array([0.025, 0.184, 0.623, 0.476, 0.817, 0.933, 0.597, 1.113, 0.728, 1.245,
        #                    0.019, 1.245, 0.647, 1.881, 0.742, 0.048, 0.418, 0.734, -0.026, -0.312])

        # y = a1√x + a2x + a3ln(x)

        self.f = [
            lambda x: sqrt(x),
            lambda x: x,
            lambda x: log(x)
        ]
        # self.f = [
        #     lambda x: 1,
        #     lambda x: x,
        #     lambda x: x**2
        # ]
        self.omega = [1 for _ in self.x]
        # self.omega = [4 if x < 1 else 1 for x in self.x]


def f(x):
    return 0.9 * log(x) - 2.1 * sqrt(x) + 0.4 * x


def least_squares(params: InputParameters):
    C = create_matrix_c(params)
    F = create_matrix_f(params)

    C_inverse = np.linalg.inv(C)
    _a = np.linalg.solve(C, F)

    R_min = calculate_r_min(params, _a)

    def _f(x):
        _sum = 0
        for k in range(params.p):
            _sum += _a[k] * params.f[k](x)
        return _sum
    # f = lambda x: _f(x) + 0.67 * calculate_eps(R_min, C_inverse, params, x)
    f = _f
    return f


def np_lstsq(params: InputParameters):
    C = create_matrix_c(params)
    F = create_matrix_f(params)

    _a = np.linalg.lstsq(C, F)[0]

    def f(x):
        _sum = 0
        for k in range(params.p):
            _sum += _a[k] * params.f[k](x)
        return _sum

    return f


def create_matrix_c(params: InputParameters):
    C = [[0 for _ in range(params.p)] for _ in range(params.p)]
    for m in range(params.p):
        for k in range(params.p):
            C_sum = 0
            for i in range(params.n):
                C_sum += params.omega[i] * params.f[m](params.x[i]) * params.f[k](params.x[i])
            C[m][k] = C_sum
    return C


def create_matrix_f(params: InputParameters):
    F = [0 for _ in range(params.p)]
    for m in range(params.p):
        F_sum = 0
        for i in range(params.n):
            F_sum += params.omega[i] * params.f[m](params.x[i]) * params.y[i]
        F[m] = F_sum
    return F


def calculate_r_min(params, _a):
    R_min = 0
    for i in range(params.n):
        y_i = params.y[i]
        for k in range(params.p):
            y_i -= _a[k] * params.f[k](params.x[i])

        R_min += params.omega[i] * y_i ** 2
    return R_min


def calculate_d(R_min, C_inverse):
    pass


def calculate_eps(R_min, C_inverse, params, x):
    _sum = 0
    for k in range(params.p):
        for m in range(params.p):
            _sum += C_inverse[k][m] * params.f[k](x) * params.f[m](x)

    eps = R_min / (params.n - params.p)
    eps *= _sum
    return abs(sqrt(eps))


if __name__ == '__main__':
    least_squares(InputParameters())
