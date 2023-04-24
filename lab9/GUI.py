from tkinter import *

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox
import matplotlib.pyplot as plt

import methods
from plot import Graph

fig = plt.Figure(figsize=(5, 5), facecolor='gainsboro')
graph = Graph(fig, title='f(x)')
params = methods.InputParameters()
interpolation = False

root = Tk()
root.wm_title(':(')
root.geometry('1680x900')
root.config(background='ghostwhite')

frame1 = Frame(root, bg='ghostwhite')
frame1.place(x=0, y=0, relwidth=0.85, relheight=1)

canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.get_tk_widget().place(x=0, y=0, relwidth=1, relheight=0.9)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.config(background='ghostwhite')
toolbar._message_label.config(background='ghostwhite')
toolbar.update()

frame2 = Frame(root, bg='ghostwhite')
frame2.place(relx=0.85, y=0, relwidth=0.15, relheight=0.9)


def on_scale(val):
    v = int(float(val))
    var.set(v)
    global params, interpolation
    params = methods.InputParameters(n=v)
    interpolation = True
    interpolate()


scale = Scale(frame2, from_=0, to=20, bg='ghostwhite', orient='horizontal', command=on_scale)
scale.place(x=10, y=85)
scale.set(params.n)
var = IntVar()


def create_labels():
    """Надписи"""
    Label(frame2, text='a - левая граница', bg='ghostwhite').place(x=10, y=10)
    Label(frame2, text='b - правая граница', bg='ghostwhite').place(x=130, y=10)
    Label(frame2, text='Количество точек', bg='ghostwhite').place(x=10, y=60)


def create_entries() -> tuple[Entry, Entry]:
    """Поля ввода"""
    entry_a = Entry(frame2, bg="ghostwhite", width=17)
    entry_b = Entry(frame2, bg="ghostwhite", width=17)

    entry_a.place(x=10, y=35)
    entry_b.place(x=130, y=35)

    entry_a.insert(0, '-1')
    entry_b.insert(0, '0')

    entry_a.bind('<Return>', interpolate)
    entry_b.bind('<Return>', interpolate)
    return entry_a, entry_b


def create_buttons():
    """Кнопки"""
    btn_run = Button(frame2, text='Интерполяция', bg='ghostwhite', command=interpolate, width=14, height=1)
    btn_quit = Button(frame2, text='Выход', bg='ghostwhite', command=_quit, width=14, height=1)

    btn_run.place(x=10, y=140)
    btn_quit.place(x=130, y=140)


def data_entry() -> methods.InputParameters | None:
    try:
        a = float(entries[0].get())
    except ValueError:
        messagebox.showerror('Error', '"a" should be a number')
        entries[0].delete(0, END)
        entries[0].insert(0, '-1')
        a = -1
    try:
        b = float(entries[1].get())
    except ValueError:
        messagebox.showerror('Error', '"b" should be a number')
        entries[1].delete(0, END)
        entries[1].insert(0, '0')
        b = 0

    if b <= a:
        messagebox.showinfo('Info', '"a" should be less than "b"')
        return
    return methods.InputParameters(a, b, var.get())


def interpolate(event=None):
    if (params := data_entry()) is not None:
        global interpolation
        if not interpolation:
            graph.clear()
            x = params.x
            y = params.y
            graph.draw_scatter(x, y, color='r')

            try:
                splines = methods.build_splines(params.x, params.y, len(params.x), params)
            except IndexError:
                messagebox.showerror('Error', 'Not enough points')
                return

            x = np.linspace(params.a, params.b, 1000)
            y = []
            for _x in x:
                y.append(methods.interpolate(splines, _x))

            graph.draw(x, y, color='black')
            interpolation = True
        else:
            graph.clear()
            x = params.x
            y = params.y
            graph.draw_scatter(x, y, color='r')
            interpolation = False
        canvas.draw()


def _quit(event=None):
    root.destroy()
    plt.close()


root.bind('<Escape>', _quit)
root.protocol('WM_DELETE_WINDOW', _quit)


def init():
    create_labels()
    create_buttons()
    global entries
    entries = create_entries()
    x = params.x
    y = params.y
    graph.draw_scatter(x, y, color='r')
