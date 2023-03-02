from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

from formulas import *
from plot import InputParameters, create_plot, fig, draw

root = Tk()
root.wm_title("Построение графиков производных")
root.geometry('1200x600')
root.config(background='ghostwhite')

frame1 = Frame(root, bg='ghostwhite')
frame1.place(x=0, y=0, relwidth=0.75, relheight=1)


canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.get_tk_widget().place(x=0, y=0, relwidth=1, relheight=0.9)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.config(background='ghostwhite')
toolbar._message_label.config(background='ghostwhite')
toolbar.update()

frame2 = Frame(root, bg='ghostwhite')
frame2.place(relx=0.75, y=0, relwidth=0.25, relheight=0.9)


def create_labels():
    """Надписи"""
    Label(frame2, text='Введите данные', bg='ghostwhite', font='Arial 12').place(x=0, y=10)
    Label(frame2, text='a', bg='ghostwhite').place(x=0, y=50)
    Label(frame2, text='b', bg='ghostwhite').place(x=100, y=50)
    Label(frame2, text='N', bg='ghostwhite').place(x=200, y=50)


def create_entries():
    """Поля ввода"""
    entry_a = Entry(frame2, bg="ghostwhite", width=15)
    entry_b = Entry(frame2, bg="ghostwhite", width=15)
    entry_N = Entry(frame2, bg="ghostwhite", width=15)

    entry_a.place(x=0, y=70)
    entry_b.place(x=100, y=70)
    entry_N.place(x=200, y=70)

    entry_a.insert(0, '-100')
    entry_b.insert(0, '1000')
    entry_N.insert(0, '1000')

    entry_a.bind('<Return>', run)
    entry_b.bind('<Return>', run)
    entry_N.bind('<Return>', run)
    return entry_a, entry_b, entry_N


def create_buttons():
    """Кнопки"""
    btn_run = Button(frame2, text='Построить', bg='ghostwhite', command=run, width=16, height=2)
    btn_quit = Button(frame2, text='Выход', bg='ghostwhite', command=_quit, width=16, height=2)

    btn_run.place(relx=1 / 5, y=120)
    btn_quit.place(relx=1 / 5, y=170)


def data_entry() -> InputParameters:
    try:
        a = float(entries[0].get())
    except ValueError:
        entries[0].delete(0, END)
        entries[0].insert(0, '-100')
        a = -100
    try:
        b = float(entries[1].get())
        if b < a:
            raise ValueError
    except ValueError:
        entries[1].delete(0, END)
        entries[1].insert(0, '1000')
        b = 1000
    try:
        N = int(entries[2].get())
        if N < 1:
            raise ValueError
    except ValueError:
        entries[2].delete(0, END)
        entries[2].insert(0, '1000')
        N = 1000
    return InputParameters(a, b, N)


def run(event=None):
    fig.clear()
    xlist, ylist_1_an, ylist_1, ylist_2, ylist_3, ylist_2_an, ylist_3_an, ylist_1_left, ylist_1_right = [], [], [], [], [], [], [], [], []

    params = data_entry()
    x = params.a

    while x < params.b:
        xlist.append(x)
        x += params.h

    for x in xlist:
        ylist_1_an.append((df_dx_an(x)))
        ylist_1.append(df_dx(x, params.h))
        ylist_2.append(d2f_dx2(x, params.h))
        ylist_2_an.append(d2f_dx2_an(x))
        ylist_3.append(d3f_dx3(x, params.h))
        ylist_3_an.append(d3f_dx3_an(x))
        ylist_1_left.append(df_dx_left(x, params.h))
        ylist_1_right.append(df_dx_right(x, params.h))

    axes = create_plot()
    draw(axes[0], xlist, ylist_1, color='black', label='числ')
    draw(axes[0], xlist, ylist_1_an, color='crimson', linestyle='--', label='анал')
    draw(axes[1], xlist, ylist_2, color='black', label='числ')
    draw(axes[1], xlist, ylist_2_an, color='crimson', linestyle='--', label='анал')
    draw(axes[2], xlist, ylist_3, color='black', label='числ')
    draw(axes[2], xlist, ylist_3_an, color='crimson', linestyle='--', label='анал')
    draw(axes[3], xlist, ylist_1_left, color='black', label='лев')
    draw(axes[3], xlist, ylist_1_right, color='crimson', linestyle='--', label='прав')

    for ax in axes:
        ax.legend()

    canvas.draw()


def _quit():
    root.destroy()
    plt.close()


if __name__ == '__main__':
    create_labels()
    entries = create_entries()
    create_buttons()
    root.mainloop()

