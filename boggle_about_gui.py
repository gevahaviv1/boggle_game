import tkinter as tk
import style_sheet as st

IMG_PATH = 'boggle_pics/'
ICON = 'boggle_pics/icon.ico'
ABOUT_TEXT = "Boggle is a hilarious word-making game that requires exceptional vocabulary.\n" \
             " Players will have three minutes to create as many words as possible from a few" \
             " jumbled-up letters.\n" \
             "Try to create long words with more letters to score more points.\n" \
             "At the end of the game, the person with the highest score will win!\n" \
             "Length: 3 minutes\n"


class BoggleAboutGui:
    def __init__(self, main_window: tk.Tk = None) -> None:
        self._main_window = main_window
        self._about_window = tk.Toplevel(self._main_window)
        self._create_about_window()

    def run(self) -> None:
        self._about_window.mainloop()

    def _create_about_window(self) -> None:
        self._about_text = ABOUT_TEXT
        st.set_window_properties(self._about_window, 'About', False, ICON, '700x300')

        tk.Label(self._about_window, text='BoggleStory', pady=20, font='Helvetica 18 bold').pack()
        tk.Label(self._about_window, text=self._about_text, pady=10).pack()
        tk.Label(self._about_window, text='Creators : Or Cohen & Geva Haviv', pady=20, font='Helvetica 10 bold').pack()

        self._about_window.transient(self._main_window)
        self._about_window.grab_set()
        self._main_window.wait_window(self._about_window)


if __name__ == '__main__':
    about = BoggleAboutGui()
    about.run()
