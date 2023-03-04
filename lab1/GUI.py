from tkinter import *
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

from formulas import *
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

    entry_a.insert(0, '-100')
    entry_b.insert(0, '1000')
    entry_N.insert(0, '1000')

    entry_a.bind('<Return>', run)
    entry_b.bind('<Return>', run)
    entry_N.bind('<Return>', run)
    return entry_a, entry_b, entry_N


def create_buttons():
    """Кнопки"""
    btn_run = Button(frame2, text='Построить', bg='ghostwhite', command=run, width=14, height=1)
    btn_quit = Button(frame2, text='Выход', bg='ghostwhite', command=_quit, width=14, height=1)

    btn_run.place(x=10, y=70)
    btn_quit.place(x=130, y=70)


def data_entry() -> InputParameters | None:
    try:
        a = float(entries[0].get())
    except ValueError:
        messagebox.showerror('Error', '"a" should be a number')
        entries[0].delete(0, END)
        entries[0].insert(0, '-100')
        a = -100
    try:
        b = float(entries[1].get())
    except ValueError:
        messagebox.showerror('Error', '"b" should be a number')
        entries[1].delete(0, END)
        entries[1].insert(0, '1000')
        b = 1000
    try:
        N = int(entries[2].get())
        if N < 1:
            raise ValueError
        elif N < 1000:
            messagebox.showwarning('Warning', '"N" is too small. The graph may be inaccurate')
    except ValueError:
        messagebox.showerror('Error', '"N" should be a int number greater than 1')
        entries[2].delete(0, END)
        entries[2].insert(0, '1000')
        N = 1000

    if b <= a:
        messagebox.showinfo('Info', '"a" should be less than "b"')
        return
    return InputParameters(a, b, N)


def run(event=None):
    if (params := data_entry()) is not None:
        fig.clear()
        first_derivative = Graph(params, 231, "f'(x)")
        left_right_first = Graph(params, 212, "left & right f'(x)")
        second_derivative = Graph(params, 232, "f''(x)")
        third_derivative = Graph(params, 233, "f'''(x)")

        first_derivative.draw(*calculate_derivative(params, df_dx), color='black', label='числ')
        first_derivative.draw(*calculate_derivative(params, df_dx_an), color='crimson', linestyle='--', label='анал')
        second_derivative.draw(*calculate_derivative(params, d2f_dx2), color='black', label='числ')
        second_derivative.draw(*calculate_derivative(params, d2f_dx2_an), color='crimson', linestyle='--', label='анал')
        third_derivative.draw(*calculate_derivative(params, d3f_dx3), color='black', label='числ')
        third_derivative.draw(*calculate_derivative(params, d3f_dx3_an), color='crimson', linestyle='--', label='анал')
        left_right_first.draw(*calculate_derivative(params, df_dx_left), color='black', label='лев')
        left_right_first.draw(*calculate_derivative(params, df_dx_right), color='crimson', linestyle='--', label='прав')

    canvas.draw()


def _quit():
    root.destroy()
    plt.close()


def init():
    create_labels()
    global entries
    entries = create_entries()
    create_buttons()
