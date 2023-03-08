from tkinter import *
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

from methods import *
from plot import InputParameters, fig, Graph

root = Tk()
root.wm_title("Построение графиков производных")
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
    Label(frame2, text='x0 - левая граница', bg='ghostwhite').place(x=10, y=10)
    Label(frame2, text='x1 - правая граница', bg='ghostwhite').place(x=130, y=10)
    Label(frame2, text='ε - точность', bg='ghostwhite').place(x=250, y=10)


def create_entries() -> tuple[Entry, Entry, Entry]:
    """Поля ввода"""
    entry_x0 = Entry(frame2, bg="ghostwhite", width=17)
    entry_x1 = Entry(frame2, bg="ghostwhite", width=17)
    entry_eps = Entry(frame2, bg="ghostwhite", width=17)

    entry_x0.place(x=10, y=35)
    entry_x1.place(x=130, y=35)
    entry_eps.place(x=250, y=35)

    entry_x0.insert(0, '-5')
    entry_x1.insert(0, '5')
    entry_eps.insert(0, '0.01')

    entry_x0.bind('<Return>', run)
    entry_x1.bind('<Return>', run)
    entry_eps.bind('<Return>', run)
    return entry_x0, entry_x1, entry_eps


def create_buttons():
    """Кнопки"""
    btn_run = Button(frame2, text='Вычислить', bg='ghostwhite', command=run, width=14, height=1)
    btn_quit = Button(frame2, text='Выход', bg='ghostwhite', command=_quit, width=14, height=1)

    btn_run.place(x=10, y=120)
    btn_quit.place(x=130, y=120)


def create_radiobuttons() -> BooleanVar:
    """Радиокнопки"""
    method = BooleanVar()
    method.set(0)
    dichotomy = Radiobutton(frame2, text='Метод дихотомии', bg='ghostwhite', variable=method, value=0)
    newton = Radiobutton(frame2, text='Метод Ньютона', bg='ghostwhite', variable=method, value=1)

    dichotomy.place(x=10, y=60)
    newton.place(x=10, y=80)
    return method


def data_entry() -> InputParameters | None:
    try:
        x0 = float(entries[0].get())
    except ValueError:
        messagebox.showerror('Error', '"x0" should be a number')
        entries[0].delete(0, END)
        entries[0].insert(0, '-5')
        x0 = -5
    try:
        x1 = float(entries[1].get())
    except ValueError:
        messagebox.showerror('Error', '"x1" should be a number')
        entries[1].delete(0, END)
        entries[1].insert(0, '5')
        x1 = 5
    try:
        eps = float(entries[2].get())
        if eps <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Error', '"ε" should be a number greater than 0')
        entries[2].delete(0, END)
        entries[2].insert(0, '0.01')
        eps = 0.01

    if x1 <= x0:
        messagebox.showinfo('Info', '"x0" should be less than "x1"')
        return
    return InputParameters(x0, x1, eps)


def run(event=None):
    if (params := data_entry()) is not None:
        fig.clear()
        graph = Graph(params, 111, "f(x)")

        graph.draw(*calculate_function(params, f), color='black')

        if method.get() == 0:
            x = dichotomy_method(f, params.x0, params.x1, params.eps)
            if x is None:
                messagebox.showerror('Метод дихотомии', f'Невозможно отыскать корень уравнения, '
                                                        f'т.к. функция не проходит через ось Ox.')
            else:
                messagebox.showinfo('Метод дихотомии', f'x ≈ {x}\t')
        else:
            x = newton_method(f, params.x0, params.eps)
            messagebox.showinfo('Метод Ньютона', f'x ≈ {x}\t')

    canvas.draw()


def _quit():
    root.destroy()
    plt.close()


def init():
    create_labels()
    global method
    method = create_radiobuttons()
    create_buttons()
    global entries
    entries = create_entries()
