import math
from tkinter import *
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

from methods import *
from plot import fig, Graph

root = Tk()
root.wm_title("Метод Рунге-Кутта")
root.geometry('1680x900')
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
    Label(frame2, text='a - левая граница', bg='ghostwhite').place(x=10, y=10)
    Label(frame2, text='b - правая граница', bg='ghostwhite').place(x=130, y=10)
    Label(frame2, text='N - количество шагов', bg='ghostwhite').place(x=250, y=10)

    Label(frame2, text='Начальные условия:', bg='ghostwhite').place(x=10, y=65)
    Label(frame2, text='y(a)', bg='ghostwhite').place(x=10, y=85)
    Label(frame2, text='z(a)', bg='ghostwhite').place(x=130, y=85)


def create_entries() -> tuple[Entry, Entry, Entry, Entry, Entry]:
    """Поля ввода"""
    entry_a = Entry(frame2, bg="ghostwhite", width=17)
    entry_b = Entry(frame2, bg="ghostwhite", width=17)
    entry_N = Entry(frame2, bg="ghostwhite", width=17)
    entry_y0 = Entry(frame2, bg="ghostwhite", width=17)
    entry_z0 = Entry(frame2, bg="ghostwhite", width=17)

    entry_a.place(x=10, y=35)
    entry_b.place(x=130, y=35)
    entry_N.place(x=250, y=35)
    entry_y0.place(x=10, y=110)
    entry_z0.place(x=130, y=110)

    entry_a.insert(0, '0')
    entry_b.insert(0, f'{math.pi}')
    entry_N.insert(0, '10000')
    entry_y0.insert(0, f'{math.pi}')
    entry_z0.insert(0, '0')

    entry_a.bind('<Return>', run)
    entry_b.bind('<Return>', run)
    entry_N.bind('<Return>', run)
    entry_y0.bind('<Return>', run)
    entry_z0.bind('<Return>', run)
    return entry_a, entry_b, entry_N, entry_y0, entry_z0


def create_buttons():
    """Кнопки"""
    btn_run = Button(frame2, text='Вычислить', bg='ghostwhite', command=run, width=14, height=1)
    btn_quit = Button(frame2, text='Выход', bg='ghostwhite', command=_quit, width=14, height=1)

    btn_run.place(x=10, y=145)
    btn_quit.place(x=130, y=145)


def data_entry() -> InputParameters | None:
    try:
        if entries[0].get() == 'pi':
            a = math.pi
        elif entries[0].get() == '-pi':
            a = -math.pi
        else:
            a = float(entries[0].get())
    except ValueError:
        messagebox.showerror('Error', '"a" should be a number')
        entries[0].delete(0, END)
        entries[0].insert(0, '0')
        a = 0
    try:
        if entries[1].get() == 'pi':
            b = math.pi
        elif entries[1].get() == '-pi':
            b = -math.pi
        else:
            b = float(entries[1].get())
    except ValueError:
        messagebox.showerror('Error', '"b" should be a number')
        entries[1].delete(0, END)
        entries[1].insert(0, f'{math.pi}')
        b = math.pi
    try:
        N = int(entries[2].get())
        if N <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Error', '"N" should be a number greater than 0')
        entries[2].delete(0, END)
        entries[2].insert(0, '10000')
        N = 10000
    try:
        if entries[3].get() == 'pi':
            y0 = math.pi
        elif entries[3].get() == '-pi':
            y0 = -math.pi
        else:
            y0 = float(entries[3].get())
    except ValueError:
        messagebox.showerror('Error', '"y0" should be a number')
        entries[3].delete(0, END)
        entries[3].insert(0, f'{math.pi}')
        y0 = math.pi
    try:
        if entries[4].get() == 'pi':
            z0 = math.pi
        elif entries[4].get() == '-pi':
            z0 = -math.pi
        else:
            z0 = float(entries[4].get())
    except ValueError:
        messagebox.showerror('Error', '"z0" should be a number')
        entries[4].delete(0, END)
        entries[4].insert(0, '0')
        z0 = 0

    if b <= a:
        messagebox.showinfo('Info', '"a" should be less than "b"')
        return
    return InputParameters(a, b, N, y0, z0)


def run(event=None):
    if (params := data_entry()) is not None:
        fig.clear()
        graph_2 = Graph(pos=121, title='2-й порядок точности')
        graph_4 = Graph(pos=122, title='4-й порядок точности')

        y2, z2 = runge_kutta_2(params)
        y4, z4 = runge_kutta_4(params)

        graph_2.draw(params.x, y2, color='black', label='y(x)')
        graph_2.draw(params.x, z2, color='red', label='z(x)')

        graph_4.draw(params.x, y4, color='black', label='y(x)')
        graph_4.draw(params.x, z4, color='red', label='z(x)')

        canvas.draw()


def _quit():
    root.destroy()
    plt.close()


def init():
    create_labels()
    create_buttons()
    global entries
    entries = create_entries()
