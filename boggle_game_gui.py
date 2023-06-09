import tkinter as tk
import boggle_board_randomizer
import style_sheet as st
import time
from typing import List, Callable, Tuple
from pygame import mixer

IMG_PATH = 'boggle_pics/'
SOUND_PATH = 'sounds/'
ICON = 'boggle_pics/icon.ico'
TIME = (3 * 60) + 1


class BoggleGameGui:
    _buttons: List[tuple] = []
    _path: List[tuple] = []

    def __init__(self) -> None:
        self._game_window = tk.Tk()
        self._game_window.wm_attributes('-alpha', 0.8)
        self._time = TIME
        self._tp_clicked = False
        self._create_game_window()
        self._update_time()

        mixer.init()
        mixer.music.load(SOUND_PATH + 'game.mp3')
        mixer.music.play(loops=-1)

    def run(self) -> None:
        self._game_window.mainloop()

    def _create_game_window(self) -> None:
        st.set_window_properties(self._game_window, 'BoggleStory', False, ICON, '1100x958+5+5')

        self.background_image = tk.PhotoImage(file=IMG_PATH + 'Game.png')
        self.label = tk.Label(self._game_window, image=self.background_image)
        self.label.place(relwidth=1, relheight=1)
        self.label.pack()

        self._game_on = True
        self._board = boggle_board_randomizer.randomize_board()
        self._create_game_window_buttons(self._game_window, st.make_button, self._board)
        self._create_game_window_labels(self._game_window)

    def _create_game_window_labels(self, window: tk.Tk) -> None:
        st.game_opening_center(window)

        # Label to display the current chosen word.
        self._display_label = tk.Label(window, font='Bodoni 20 bold', fg='white', bg='black', height=2, width=27)
        self._display_label.place(x=280, y=160)

        # Label to display the current time.
        self._time_label = tk.Label(window, font='Bodoni 20 bold', fg='white', bg='#b91606', height=1,
                                    width=4)
        self._time_label.place(x=493, y=105)

        # Label to display the exposed words.
        self._words_label = tk.Label(window, font='Bodoni 12 bold', bg='#b91606', height=8, width=30, anchor='n')
        self._words_label.place(x=380, y=725)

        # Label to display the score.
        self._score_label = tk.Label(window, text='Score: 0', bg='#b91606', font='Bodoni 11 bold',
                                     height=0, width=10)
        self._score_label.place(x=457, y=917)

    def _create_game_window_buttons(self, window: tk.Tk, func, board: List[List[str]]) -> None:
        # Board buttons.
        self._buttons = [(board[j][i], func(window, board[j][i], (i * 120) + 280, (j * 90) + 250, 'BUTTON_STYLE_BOARD'),
                          (j, i)) for i in range(len(board)) for j in range(len(board[i]))]
        # Undo button.
        self._buttons.append(('Undo', func(self._game_window, 'Undo', 280, 620, 'BUTTON_STYLE'), (4, 0)))
        # Clear button.
        self._buttons.append(('Clear', func(self._game_window, 'Clear', 400, 620, 'BUTTON_STYLE'), (4, 1)))
        # Add button.
        self._buttons.append(('Add', func(self._game_window, 'Add', 650, 620, 'BUTTON_STYLE'), (4, 2)))

    def get_buttons(self) -> List[Tuple[str, tk.Button, Tuple[int, int]]]:
        return [key for key in self._buttons]

    def get_board(self) -> List[str]:
        return self._board

    def set_button_command(self, coordinate: Tuple[int, int], cmd: Callable[[], None]) -> None:
        [key[1].configure(command=cmd) for key in self._buttons if key[2] == coordinate]

    def set_display(self, display_text: str) -> None:
        self._display_label['text'] = display_text

    def set_expose_words(self, exposed_words: str) -> None:
        self._words_label['text'] = exposed_words

    def set_score(self, score: int) -> None:
        self._score_label['text'] = 'Score: ' + str(score)

    def _update_time(self) -> None:
        if self._time == 0:
            self._game_on = False
            self._create_tp()

        if self._game_on:
            self._time -= 1
            text = int(self._time / 60), ':', self._time % 60
            self._time_label.configure(text=text, font='Ariel 12 bold')
            self._game_window.after(1000, self._update_time)

    def _create_tp(self) -> None:
        self._tp = tk.Toplevel(self._game_window)
        self._tp.geometry('300x100')
        self._tp.iconbitmap(ICON)

        tk.Label(self._tp, text='Do you want to play again?', pady=20, font='Helvetica 10 bold').pack()
        no = tk.Button(self._tp, text='No', command=self._destroy_game)
        no.place(x=150, y=50)
        yes = tk.Button(self._tp, text='Yes', command=self._new_game)
        yes.place(x=110, y=50)

        self._tp.transient(self._game_window)
        self._tp.grab_set()
        self._game_window.wait_window(self._tp)

    def _new_game(self) -> None:
        mixer.Channel(0).play(mixer.Sound(SOUND_PATH + 'click.mp3'))
        self._tp.destroy()
        self._tp_clicked = True
        self._game_window.destroy()

    def _destroy_game(self) -> None:
        mixer.Channel(0).play(mixer.Sound(SOUND_PATH + 'click.mp3'))
        time.sleep(0.4)
        self._tp_clicked = False
        self._game_window.destroy()

    def get_tp_clicked(self) -> bool:
        return self._tp_clicked


if __name__ == '__main__':
    game = BoggleGameGui()
    game.run()
