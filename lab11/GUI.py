from tkinter import *
from tkinter import messagebox, Entry

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

from methods import *
from plot import fig, Graph

root = Tk()
root.wm_title("Ряды Фурье")
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
    Label(frame2, text='x1', bg='ghostwhite').place(x=160, y=10)

    Label(frame2, text='Количество гармоник m', bg='ghostwhite').place(x=10, y=60)
    Label(frame2, text='Остаточная дисперсия Q', bg='ghostwhite').place(x=160, y=60)
    label_q = Label(frame2, text='', bg='ghostwhite')
    label_q.place(x=160, y=80)
    return label_q


def create_entries() -> tuple[Entry, Entry, Entry]:
    """Поля ввода"""
    entry_x0 = Entry(frame2, bg="ghostwhite", width=17)
    entry_x1 = Entry(frame2, bg="ghostwhite", width=17)
    entry_m = Entry(frame2, bg="ghostwhite", width=17)

    entry_x0.place(x=10, y=30)
    entry_x1.place(x=160, y=30)
    entry_m.place(x=10, y=80)

    entry_x0.insert(0, f'{-np.pi}')
    entry_x1.insert(0, f'{np.pi}')
    entry_m.insert(0, '1000')

    return entry_x0, entry_x1, entry_m


def create_buttons():
    """Кнопки"""
    btn_run = Button(frame2, text='Вычислить', bg='ghostwhite', command=run, width=14, height=1)
    btn_quit = Button(frame2, text='Выход', bg='ghostwhite', command=_quit, width=14, height=1)
    btn_graph = Button(frame2, text='Графики', bg='ghostwhite', command=graph, width=14, height=1)
    btn_chart = Button(frame2, text='Диаграммы', bg='ghostwhite', command=chart, width=14, height=1)

    btn_run.place(x=10, y=125)
    btn_quit.place(x=130, y=125)
    btn_graph.place(x=10, y=160)
    btn_chart.place(x=130, y=160)


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
        m = int(entries[2].get())
    except ValueError:
        messagebox.showerror('Error', '"m" should be an int number')
        entries[2].delete(0, END)
        entries[2].insert(0, '1000')
        m = 1000

    if x1 <= x0:
        messagebox.showinfo('Info', '"x0" should be less than "x1"')
        return
    return InputParameters(x0, x1, m)


global a, b, y, A, freq


def graph(event=None):
    if (params := data_entry()) is not None:
        fig.clear()
        graph_orig = Graph(pos=121, title='y(x)')
        graph_image = Graph(pos=122, title='Ряд Фурье')

        graph_orig.draw(params.x, params.y, color='black')
        graph_image.draw(params.x, y, color='black')
        canvas.draw()


def chart(event=None):
    if (params := data_entry()) is not None:
        fig.clear()
        graph_A = Graph(pos=121, title='Амплитуды')
        graph_freq = Graph(pos=122, title='Частоты')

        graph_A.chart([k for k in range(1, params.m + 1)], A, color='black')
        graph_freq.chart([k for k in range(1, params.m + 1)], freq, color='black')
        canvas.draw()


def run(event=None):
    if (params := data_entry()) is not None:
        global a, b, y, A, freq

        a, b = furier_coeffs(params.x, params.y, params.freq, params.m)
        y = [furier_series(x, a, b, params.freq, params.m) for x in params.x]

        label_q['text'] = dispersion(params.y, y)

        A = []
        freq = []
        for k in range(1, params.m + 1):
            A.append(sqrt(a[k] ** 2 + b[k] ** 2))
            freq.append(params.freq * k)

        print(A)


def _quit(event=None):
    root.destroy()
    plt.close()


def bind():
    for entry in entries:
        entry.bind('<Return>', run)

    root.bind('<Escape>', _quit)
    root.protocol('WM_DELETE_WINDOW', _quit)


def init():
    global entries, label_q
    label_q = create_labels()
    create_buttons()
    entries = create_entries()
    bind()
    run()
