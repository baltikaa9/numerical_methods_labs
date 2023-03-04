from dataclasses import dataclass

import matplotlib.pyplot as plt

fig = plt.Figure(figsize=(5, 5), facecolor='gainsboro')


@dataclass
class InputParameters:
    a: float
    b: float
    N: int

    def __post_init__(self):
        self.h = (self.b - self.a) / self.N


class Graph:
    def __init__(self, params: InputParameters, pos: int, title: str):
        self.params = params
        self.ax = fig.add_subplot(pos)
        self.ax.set(title=title,
                    xlabel='x',
                    ylabel='y',
                    facecolor='ghostwhite')
        self.ax.grid()

    def draw(self, x: list, y: list, **kwargs):
        self.ax.plot(x, y, **kwargs)
        self.ax.legend()
