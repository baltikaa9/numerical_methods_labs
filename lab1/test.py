import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import numpy as np


def _quit():
    root.quit()  # остановка цикла
    root.destroy()  # закрытие приложения


root = tkinter.Tk()
root.wm_title("Построение графика y=sin(x)")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.linspace(0, 2 * np.pi)
ax = fig.add_subplot(111)
ax.plot(t, np.sin(t), '-rh', linewidth=3, markersize=5, markerfacecolor='b',
     label=r'$\ y=sin(x) $')
ax.grid(color='b', linewidth=1.0)
ax.legend(fontsize=12)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

button = tkinter.Button(master=root, text="Выход", command=_quit)
button.pack(side=tkinter.BOTTOM)



if __name__ == '__main__':
    tkinter.mainloop()
