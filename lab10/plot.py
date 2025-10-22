from typing import Any

import matplotlib.pyplot as plt

fig = plt.Figure(figsize=(5, 5), facecolor='gainsboro')


class Graph:
    def __init__(self, pos: int = None, title: str = 'f(x)'):
        self.ax = fig.add_subplot(pos) if pos is not None else fig.add_subplot()
        self.ax.set(title=title,
                    xlabel='x',
                    ylabel='y',
                    facecolor='ghostwhite')
        self.ax.grid()

    def draw(self, x: list[float] | Any, y: list[float] | Any, **kwargs):
        self.ax.plot(x, y, **kwargs)
        if 'label' in kwargs:
            self.ax.legend(loc='lower left')

    def scatter(self, x: float, y: float, **kwargs):
        self.ax.scatter(x, y, **kwargs)
