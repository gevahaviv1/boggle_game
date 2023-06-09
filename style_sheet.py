import tkinter as tk
from typing import Any

PATH = 'boggle_pics/'
ICON = 'boggle_pics/icon.ico'
BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'black'
BUTTON_ACTIVE_COLOR = '#b91606'
BUTTON_STYLE = {"font": ("Courier", 20), "width": 5, "height": 1, "borderwidth": 1, "relief": tk.RAISED,
                "bg": REGULAR_COLOR, "fg": 'white', "activebackground": BUTTON_ACTIVE_COLOR}
BUTTON_STYLE_BOARD = {"font": ("Courier", 30), "width": 4, "height": 1, "borderwidth": 1, "relief": tk.RAISED,
                      "bg": REGULAR_COLOR, "fg": 'white', "activebackground": BUTTON_ACTIVE_COLOR}


def make_button(window: tk.Tk, button_char: str, row: int, col: int, button_style: str) -> tk.Button:
    if button_style == 'BUTTON_STYLE_BOARD':
        button_style = BUTTON_STYLE_BOARD
    else:
        button_style = BUTTON_STYLE

    button = tk.Button(window, text=button_char, **button_style)
    button.place(x=row, y=col)

    def _on_enter(event: Any) -> None:
        button['background'] = BUTTON_HOVER_COLOR

    def _on_leave(event: Any) -> None:
        button['background'] = REGULAR_COLOR

    button.bind("<Enter>", _on_enter)
    button.bind("<Leave>", _on_leave)
    return button


def set_window_properties(window: tk.Tk or tk.Toplevel, title: str, resizable: bool, icon: str, geometry: str) -> None:
    window.title(title)
    window.resizable(resizable, resizable)
    window.iconbitmap(icon)
    window.geometry(geometry)


def game_opening_center(game_window) -> None:
    game_window.update_idletasks()
    width = game_window.winfo_width()
    frm_width = game_window.winfo_rootx() - game_window.winfo_x()
    win_width = width + 2 * frm_width
    height = game_window.winfo_height()
    bar_height = game_window.winfo_rooty() - game_window.winfo_y()
    win_height = height + bar_height + frm_width
    x = game_window.winfo_screenwidth() // 2 - win_width // 2
    y = game_window.winfo_screenheight() // 2 - win_height // 2
    game_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    game_window.deiconify()


