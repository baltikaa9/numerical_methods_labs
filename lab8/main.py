# from GUI import init, root
#
# if __name__ == '__main__':
#     init()
#     root.mainloop()

import matplotlib.pyplot as plt

from methods import *
from plot import Graph

fig = plt.figure(facecolor='gainsboro')

if __name__ == '__main__':
    params = InputParameters()
    graph = Graph(fig, title='f(x)')

    for i in range(params.n):
        graph.draw_scatter(params.x[i], params.y[i], c='red')

    f_ = least_squares(params)
    x = np.linspace(1, 21, params.n)
    y = [f_(x) for x in x]
    graph.draw(x, y, color='black', label='Решение МНК')

    x = np.linspace(1, 21, 100)
    y = [f(x) for x in x]
    graph.draw(x, y, color='purple', label='Точное решение')

    # np_x = np.linspace(1, 21, params.n)
    # np_f_ = np_lstsq(params)
    # np_y = [np_f_(x) for x in np_x]
    # graph.draw(np_x, np_y, color='g')

    plt.show()
