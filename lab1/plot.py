from dataclasses import dataclass

import matplotlib.pyplot as plt

fig = plt.Figure(figsize=(5, 5), facecolor='ghostwhite')


@dataclass
class InputParameters:
    a: float
    b: float
    N: int

    def __post_init__(self):
        self.h = (self.b - self.a) / self.N


def create_plot():
    ax_1 = fig.add_subplot(131)
    ax_1.set(title="f'(x)",
             xlabel='x',
             ylabel='y',
             facecolor='ghostwhite')
    ax_1.grid()
    ax_2 = fig.add_subplot(132)
    ax_2.set(title="f''(x)",
             xlabel='x',
             ylabel='y',
             facecolor='ghostwhite')
    ax_2.grid()
    ax_3 = fig.add_subplot(133)
    ax_3.set(title="f'''(x)",
             xlabel='x',
             ylabel='y',
             facecolor='ghostwhite')
    ax_3.grid()
    return [ax_1, ax_2, ax_3]


def draw(ax, x, y, **kwargs):
    ax.plot(x, y, **kwargs)
