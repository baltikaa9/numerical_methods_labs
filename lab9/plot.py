import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class Graph:
    def __init__(self, fig, title: str = 'f(x)'):
        self.fig = fig
        self.ax = fig.add_subplot()
        self.ax.set(title=title,
                    xlabel='x',
                    ylabel='y',
                    facecolor='ghostwhite')
        self.ax.grid()

    def draw(self, x: list, y: list, **kwargs):
        self.ax.plot(x, y, **kwargs)
        if 'label' in kwargs:
            self.ax.legend()

    def draw_scatter(self, x, y, **kwargs):
        self.ax.scatter(x, y, **kwargs)

    def clear(self):
        self.ax.clear()
        self.ax.grid()
