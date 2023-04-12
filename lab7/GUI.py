from tkinter import *
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

from methods import *
from plot import Graph

fig = plt.Figure(figsize=(5, 5), facecolor='gainsboro')

root = Tk()
root.wm_title(':(')
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


def create_entries() -> tuple[Entry, Entry, Entry]:
    """Поля ввода"""
    entry_a = Entry(frame2, bg="ghostwhite", width=17)
    entry_b = Entry(frame2, bg="ghostwhite", width=17)
    entry_N = Entry(frame2, bg="ghostwhite", width=17)

    entry_a.place(x=10, y=35)
    entry_b.place(x=130, y=35)
    entry_N.place(x=250, y=35)

    entry_a.insert(0, '-10')
    entry_b.insert(0, '10')
    entry_N.insert(0, '1000')

    entry_a.bind('<Return>', run)
    entry_b.bind('<Return>', run)
    entry_N.bind('<Return>', run)
    return entry_a, entry_b, entry_N


def create_buttons():
    """Кнопки"""
    btn_run = Button(frame2, text='Вычислить', bg='ghostwhite', command=run, width=14, height=1)
    btn_quit = Button(frame2, text='Выход', bg='ghostwhite', command=_quit, width=14, height=1)

    btn_run.place(x=10, y=140)
    btn_quit.place(x=130, y=140)


def create_radiobuttons() -> IntVar:
    """Радиокнопки"""
    method = IntVar()
    method.set(1)
    min = Radiobutton(frame2, text='Минимум', bg='ghostwhite', variable=method, value=1)
    max = Radiobutton(frame2, text='Максимум', bg='ghostwhite', variable=method, value=0)

    min.place(x=10, y=60)
    max.place(x=10, y=80)
    return method


def data_entry() -> InputParameters | None:
    try:
        a = float(entries[0].get())
    except ValueError:
        messagebox.showerror('Error', '"a" should be a number')
        entries[0].delete(0, END)
        entries[0].insert(0, '0')
        a = 0
    try:
        b = float(entries[1].get())
    except ValueError:
        messagebox.showerror('Error', '"b" should be a number')
        entries[1].delete(0, END)
        entries[1].insert(0, '1')
        b = 1
    try:
        N = int(entries[2].get())
        if N <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Error', '"N" should be a number greater than 0')
        entries[2].delete(0, END)
        entries[2].insert(0, '10000')
        N = 10000

    if b <= a:
        messagebox.showinfo('Info', '"a" should be less than "b"')
        return
    return InputParameters(a, b, N)


def run(event=None):
    if (params := data_entry()) is not None:
        fig.clear()
        graph = Graph(fig, title='F(x, y)')

        graph.draw(params.x, params.y, params.z, color='black')

        x, y = gradient_descent(graph)
        graph.draw_scatter(x, y, F(x, y), color='r')
        print(x, (3-x)/2, sqrt(F(x, y)))

        canvas.draw()


def _quit():
    root.destroy()
    plt.close()


def init():
    create_labels()
    create_buttons()
    global entries
    entries = create_entries()
