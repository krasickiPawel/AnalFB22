import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.image as mpimg
import os
from statistics_conversation import ConversationStatistics
from statistics_full_messenger import FullMessengerStatistics
from statistics import Statistics
from statistics_interface import StatisticsInterface
import settings
from file_reader import get_conversation_dir_name_dict
from threading import Thread
import ctypes as ct

root = tk.Tk()
label_status_string_var = tk.StringVar()
chart_list = []
statistics_interface = None
inbox = None
conversation_name_path_dict = dict()
# threading.Thread(target=get_conversation_dir_name_dict, args=(conversation_name_path_dict,)).start()


def dark_title_bar(window, mode=2):
    """
    setting window title bar to dark mode
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    val = mode
    val = ct.c_int(val)
    set_window_attribute(hwnd, 20, ct.byref(val), 4)


def calculate_conversation_command():
    root.after(10, calculate_statistics, ConversationStatistics)


def calculate_full_messenger_command():
    root.after(10, calculate_statistics, FullMessengerStatistics)


def calculate_statistics(statistics_class: Statistics):
    print(statistics_class)
    # unpack_plot()
    # label z info zeby podac folder
    dir_path = filedialog.askdirectory()
    if not os.path.exists(dir_path):
        # label z info ze taki folder nie istnieje
        return
    set_save_button_disabled()
    set_run_buttons_disabled()
    # wczytywanie pasek postepu i sciezki plikow
    stat = statistics_class.from_dir(dir_path)
    print(type(stat))
    stat.calculate()
    res_dict = stat.get_res_dict()
    print(res_dict)
    # przetwarzanie z paskiem postepu podzielonym na ilosc funkcji
    # append wykresow do listy do zapisu
    # settings.result_lines.append(info_to_be_saved)
    set_save_button_enabled()
    # usuniecie obecnego frame i pokazanie tego z pyplotem a na dole pasek wielu pozostalych zdjec albo dwa przyciski next back
    # pack_plot(img_path, info, is_cancer)
    set_run_buttons_enabled()


def save_results():
    save_dir_path = filedialog.askdirectory()
    # settings.result_lines = []
    set_save_button_disabled()


def set_save_button_enabled():
    button_save.config(state="normal")
    root.update()


def set_save_button_disabled():
    button_save.config(state="disabled")
    root.update()


def set_run_buttons_enabled():
    button_conv.config(state="normal")
    button_full_msgr.config(state="normal")
    root.update()


def set_run_buttons_disabled():
    button_conv.config(state="disabled")
    button_full_msgr.config(state="disabled")
    root.update()



# def unpack_plot_command():
#     if settings.figs.get("fig_tk"):
#         settings.figs["fig_tk"].place_forget()
#         del(settings.figs["fig_tk"])
#     if settings.toolbars.get("toolbar"):
#         settings.toolbars["toolbar"].destroy()
#     button_close_canvas.place_forget()
#     text_results.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
#     root.update()


# def pack_plot(img_path, x_label_txt, is_cancer=True):
    # plt.rcParams['figure.facecolor'] = settings.general_bg
    # plt.rcParams['axes.facecolor'] = settings.general_bg
    #
    # x_label_txt = f"{x_label_txt}\n"
    # text_results.place_forget()
    # fig = plt.figure(figsize=(6, 6), dpi=100)
    # figure_canvas = FigureCanvasTkAgg(fig, frame_results)
    # fig_tk = figure_canvas.get_tk_widget()
    #
    # toolbar = NavigationToolbar2Tk(figure_canvas, frame_results)
    # toolbar.config(background=settings.general_bg)
    # toolbar._message_label.config(background='grey')
    # toolbar.update()
    #
    # img = mpimg.imread(img_path)
    # red_font_dict = {'family': 'arial', 'color': '#F44336', 'weight': 'normal', 'size': 12}
    # green_font_dict = {'family': 'arial', 'color': '#32CD32', 'weight': 'normal', 'size': 12}
    # font_dict = red_font_dict if is_cancer else green_font_dict
    #
    # ax = fig.add_subplot(1, 1, 1)
    # ax.set_title(img_path, color=settings.general_fg)
    # ax.spines['bottom'].set_color(settings.general_fg)
    # ax.tick_params(axis='x', colors=settings.general_fg)
    # ax.spines['left'].set_color(settings.general_fg)
    # ax.tick_params(axis='y', colors=settings.general_fg)
    # ax.spines['right'].set_color(settings.general_bg)
    # ax.spines['top'].set_color(settings.general_bg)
    # ax.set_xlabel(x_label_txt, fontdict=font_dict)
    # ax.imshow(img)
    # root.update()
    #
    # fig_tk.place(relx=0.0, rely=0.05, relwidth=0.9, relheight=0.85)
    # toolbar.place(relx=0.5, rely=0.95, relwidth=0.5, relheight=0.05, anchor="center")
    #
    # button_close_canvas.place(relx=0.91, rely=0.05, relwidth=0.04, relheight=0.02)
    #
    # settings.figs["fig_tk"] = fig_tk
    # settings.toolbars["toolbar"] = toolbar


def toggle_fullscreen(event):
    root.attributes("-fullscreen", True)


def end_fullscreen(event):
    root.attributes("-fullscreen", False)


def label_status_update(event):
    label_status_string_var.set(event)


def button_on_enter(e):
    e.widget['background'] = 'lightgrey'


def button_on_leave(e):
    e.widget['background'] = 'SystemButtonFace'


frame_control_panel = tk.Frame(root, bg=settings.COLORS.get("bg"))
frame_control_panel.place(relx=0.01, rely=0.0, relwidth=0.2, relheight=1)

frame_control_conversations = tk.Frame(frame_control_panel, bg=settings.COLORS.get("bg"))
frame_control_conversations.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.6)

frame_control_buttons = tk.Frame(frame_control_panel, bg=settings.COLORS.get("bg"))
frame_control_buttons.place(relx=0.0, rely=0.6, relwidth=1, relheight=0.4)

frame_results = tk.Frame(root, bg=settings.COLORS.get("bg"))
frame_results.place(relx=0.21, rely=0.0, relwidth=0.79, relheight=1)

frame_results_control_panel = tk.Frame(frame_results, bg=settings.COLORS.get("bg"))
frame_results_control_panel.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)


def select_inbox():
    global conversation_name_path_dict
    global inbox
    dir_path = filedialog.askdirectory()
    if not os.path.exists(dir_path):
        # label z info ze taki folder nie istnieje
        return
    inbox = dir_path
    set_save_button_disabled()
    set_run_buttons_disabled()
    conversation_name_path_dict = get_conversation_dir_name_dict(inbox)
    conversation_name_path_dict.pop("")
    # wczytywanie pasek postepu i sciezki plikow
    items = list(conversation_name_path_dict.keys())
    print(items[:3])
    conversation_listbox_items.set(value=items)
    set_save_button_enabled()
    set_run_buttons_enabled()


button_select_inbox = tk.Button(
    frame_control_conversations,
    text=settings.TEXTS.get("button_select_inbox"),
    bg=settings.COLORS.get("bg"),
    fg=settings.COLORS.get("fg"),
    font=settings.FONTS.get("button"),
    command=Thread(target=select_inbox).start,
    borderwidth=0,
    activebackground=settings.COLORS.get("bg")
)
button_select_inbox.place(relx=0, rely=0.05, relwidth=1, relheight=0.1)
button_select_inbox.bind("<Motion>", button_on_enter)
button_select_inbox.bind("<Leave>", button_on_leave)


def listbox_on_double(event):
    Thread(target=listbox_on_double_thread).start()


def listbox_on_double_thread():
    global chart_list
    selected_key = conversation_listbox.get(conversation_listbox.curselection())
    conversation_path = conversation_name_path_dict.get(selected_key)
    set_save_button_disabled()
    set_run_buttons_disabled()
    stat = StatisticsInterface.from_dir(ConversationStatistics, conversation_path)
    stat.calculate()
    chart_list = stat.get_chart_list()
    set_save_button_enabled()
    set_run_buttons_enabled()


conversation_listbox_items = tk.Variable()
conversation_listbox = tk.Listbox(
    frame_control_conversations,
    listvariable=conversation_listbox_items,
    bg=settings.COLORS.get("listbox_bg"),
    fg=settings.COLORS.get("listbox_fg"),
    font=settings.FONTS.get("listbox"),
    borderwidth=0,
    activestyle="none",
    disabledforeground="grey",
    highlightbackground="green",
    highlightcolor="red",
    selectbackground="lightgrey",
    selectforeground="black",
)
conversation_listbox.place(relx=0, rely=0.16, relwidth=1, relheight=0.5)
conversation_listbox.bind("<Double-Button>", listbox_on_double)

button_conv = tk.Button(
    frame_control_buttons,
    text=settings.TEXTS.get("button_conv"),
    bg=settings.COLORS.get("bg"),
    fg=settings.COLORS.get("fg"),
    font=settings.FONTS.get("button"),
    command=calculate_conversation_command,
    borderwidth=0,
    activebackground=settings.COLORS.get("bg")
)
button_conv.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)
button_conv.bind("<Enter>", button_on_enter)
button_conv.bind("<Leave>", button_on_leave)

button_full_msgr = tk.Button(
    frame_control_buttons,
    text=settings.TEXTS.get("button_full_msgr"),
    bg=settings.COLORS.get("bg"),
    fg=settings.COLORS.get("fg"),
    font=settings.FONTS.get("button"),
    command=calculate_full_messenger_command,
    borderwidth=0,
    activebackground=settings.COLORS.get("bg")
)
button_full_msgr.place(relx=0, rely=0.2, relwidth=1, relheight=0.1)
button_full_msgr.bind("<Enter>", button_on_enter)
button_full_msgr.bind("<Leave>", button_on_leave)


count = 0


def test_plots():
    global count
    chart = chart_list[count]
    chart.show()
    count += 1


button_without_groups = tk.Button(
    frame_control_buttons,
    text=settings.TEXTS.get("button_without_groups"),
    bg=settings.COLORS.get("bg"),
    fg=settings.COLORS.get("fg"),
    font=settings.FONTS.get("button"),
    command=test_plots,
    borderwidth=0,
    activebackground=settings.COLORS.get("bg")
)
button_without_groups.place(relx=0, rely=0.3, relwidth=1, relheight=0.1)
button_without_groups.bind("<Enter>", button_on_enter)
button_without_groups.bind("<Leave>", button_on_leave)

button_save = tk.Button(
    frame_control_buttons,
    text=settings.TEXTS.get("button_save").title(),
    bg=settings.COLORS.get("bg"),
    fg=settings.COLORS.get("fg"),
    font=settings.FONTS.get("button"),
    command=calculate_full_messenger_command,
    borderwidth=0,
    activebackground=settings.COLORS.get("bg")
)
button_save.place(relx=0, rely=0.4, relwidth=1, relheight=0.1)
button_save.bind("<Enter>", button_on_enter)
button_save.bind("<Leave>", button_on_leave)

label_status = tk.Label(
    frame_results,
    fg=settings.COLORS.get("fg"),
    bg=settings.COLORS.get("bg"),
    textvariable=label_status_string_var,
)
label_status.place(relx=0.5, rely=0.5, anchor="center")


root.title(settings.WINDOW_SETTINGS.get("title"))
root.geometry(settings.WINDOW_SETTINGS.get("geometry"))
root.state('zoomed')
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)
root.bind("<<label_status_update>>", label_status_update)
root.minsize(960, 540)


def run():
    set_save_button_disabled()
    root.mainloop()


if __name__ == '__main__':
    run()

