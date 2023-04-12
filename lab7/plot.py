import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class Graph:
    def __init__(self, fig, title: str = 'f(x)'):
        self.fig = fig
        self.ax = Axes3D(self.fig)
        self.ax.set(title=title,
                    xlabel='x',
                    ylabel='y',
                    zlabel='z',
                    facecolor='ghostwhite')

    def draw(self, x: list, y: list, z: list, **kwargs):
        x, y = np.meshgrid(x, y)
        z = np.array(z)
        self.ax.plot_surface(x, y, z, **kwargs)
        # self.ax.legend()

    def draw_scatter(self, x, y, z, **kwargs):
        self.ax.scatter(x, y, z, **kwargs)
