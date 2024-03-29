import matplotlib.pyplot as plt

fig = plt.Figure(figsize=(5, 5), facecolor='gainsboro')


class Graph:
    def __init__(self, pos: int, title: str):
        self.ax = fig.add_subplot(pos) if pos is not None else fig.add_subplot()
        self.ax.set(title=title,
                    xlabel='x',
                    ylabel='y',
                    facecolor='ghostwhite')
        self.ax.grid()

    def draw(self, x: list, y: list, **kwargs):
        self.ax.plot(x, y, **kwargs)
        # self.ax.legend()

    def draw_Ox(self, left, right):
        x = [x for x in range(int(left), int(right + 1))]
        y = [0] * int(right - left + 1)
        self.draw(x, y, color='black')
