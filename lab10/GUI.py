from tkinter import *
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

from .methods import *
from .plot import fig, Graph

root = Tk()
root.wm_title("Метод стрельбы")
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
    Label(frame2, text='x0', bg='ghostwhite').place(x=10, y=10)
    Label(frame2, text='x1', bg='ghostwhite').place(x=130, y=10)

    Label(frame2, text='y(x0)', bg='ghostwhite').place(x=10, y=60)
    Label(frame2, text='y(x1)', bg='ghostwhite').place(x=130, y=60)


def create_entries() -> tuple[Entry, Entry, Entry, Entry]:
    """Поля ввода"""
    entry_x0 = Entry(frame2, bg="ghostwhite", width=17)
    entry_x1 = Entry(frame2, bg="ghostwhite", width=17)
    entry_y0 = Entry(frame2, bg="ghostwhite", width=17)
    entry_y1 = Entry(frame2, bg="ghostwhite", width=17)

    entry_x0.place(x=10, y=30)
    entry_x1.place(x=130, y=30)
    entry_y0.place(x=10, y=80)
    entry_y1.place(x=130, y=80)

    entry_x0.insert(0, '0')
    entry_x1.insert(0, '1')
    entry_y0.insert(0, '0')
    entry_y1.insert(0, '-1')

    return entry_x0, entry_x1, entry_y0, entry_y1


def create_buttons():
    """Кнопки"""
    btn_run = Button(frame2, text='Вычислить', bg='ghostwhite', command=run, width=14, height=1)
    btn_quit = Button(frame2, text='Выход', bg='ghostwhite', command=_quit, width=14, height=1)

    btn_run.place(x=10, y=125)
    btn_quit.place(x=130, y=125)


def data_entry() -> InputParameters | None:
    try:
        x0 = float(entries[0].get())
    except ValueError:
        messagebox.showerror('Error', '"x0" should be a number')
        entries[0].delete(0, END)
        entries[0].insert(0, '0')
        x0 = 0
    try:
        x1 = float(entries[1].get())
    except ValueError:
        messagebox.showerror('Error', '"x1" should be a number')
        entries[1].delete(0, END)
        entries[1].insert(0, '1')
        x1 = 1
    try:
        y0 = float(entries[2].get())
    except ValueError:
        messagebox.showerror('Error', '"y(x0)" should be a number')
        entries[2].delete(0, END)
        entries[2].insert(0, '0')
        y0 = 0
    try:
        y1 = float(entries[3].get())
    except ValueError:
        messagebox.showerror('Error', '"y(x1)" should be a number')
        entries[3].delete(0, END)
        entries[3].insert(0, '-1')
        y1 = -1

    if x1 <= x0:
        messagebox.showinfo('Info', '"x0" should be less than "x1"')
        return
    return InputParameters(x0, x1, y0, y1)


def run(event=None):
    if (params := data_entry()) is not None:
        fig.clear()
        graph = Graph(title='y(x)')

        try:
            y, attemps = shooting_method(params)
        except ValueError as err:
            messagebox.showerror('Error', err)
            return

        for i, attemp in enumerate(attemps):
            graph.draw(params.x, attemp, linestyle='dashed', label=f'Попытка {i}')

        graph.draw(params.x, y, color='black', label='Результат')

        graph.scatter(params.x1, params.y1, color='red', s=100)

        canvas.draw()


def _quit(event=None):
    root.destroy()
    plt.close()


def bind():
    for entry in entries:
        entry.bind('<Return>', run)

    root.bind('<Escape>', _quit)
    root.protocol('WM_DELETE_WINDOW', _quit)



def init():
    create_labels()
    create_buttons()
    global entries
    entries = create_entries()
    bind()
