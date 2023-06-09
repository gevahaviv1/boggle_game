import tkinter as tk
import style_sheet as st
import time
from boggle_about_gui import BoggleAboutGui
from pygame import mixer

IMG_PATH = 'boggle_pics/'
SOUND_PATH = 'sounds/'
ICON = 'boggle_pics/icon.ico'


class BoggleOpenGui:
    def __init__(self) -> None:
        root = tk.Tk()
        self._opening = root
        self._opening.wm_attributes('-alpha', 0.8)
        self._start = False
        self._about_window = None
        mixer.init()
        mixer.music.load(SOUND_PATH + 'opening.mp3')
        mixer.music.play(loops=-1)

    def run(self) -> None:
        self._create_main_window()
        self._opening.mainloop()

    def _create_main_window(self) -> None:
        st.set_window_properties(self._opening, 'BoggleStory', False, ICON, '1054x470')

        self.background_image = tk.PhotoImage(file=IMG_PATH + 'boggle_logo.png')
        self.label = tk.Label(self._opening, image=self.background_image)
        self.label.place(relwidth=1, relheight=1)
        self.label.pack()

        self._create_main_window_buttons()

    def _create_main_window_buttons(self) -> None:
        self._about_button_pic = tk.PhotoImage(file=IMG_PATH + 'about_button.png')
        self._start_button_pic = tk.PhotoImage(file=IMG_PATH + 'start_button.png')
        self._quit_button_pic = tk.PhotoImage(file=IMG_PATH + 'quit_button.png')

        self._quit_button = tk.Button(self._opening, image=self._quit_button_pic, command=self._destroy_game,
                                      bg='black')
        self._quit_button.place(x=460, y=400)
        self._about_button = tk.Button(self._opening, image=self._about_button_pic, bg='black',
                                       command=self._run_about_window)
        self._about_button.place(x=460, y=340)
        self._start_button = tk.Button(image=self._start_button_pic, bg='black',
                                       command=lambda c='Start': self._click_btn(c))
        self._start_button.place(x=460, y=280)

    def get_start(self) -> bool:
        return self._start

    def _destroy_game(self) -> None:
        mixer.Channel(0).play(mixer.Sound(SOUND_PATH + 'click.mp3'))
        time.sleep(0.5)
        self._opening.destroy()

    def _click_btn(self, c):
        if c == 'Start':
            mixer.Channel(0).play(mixer.Sound(SOUND_PATH + 'click.mp3'))
            self._start = True
            self._opening.destroy()

    def _run_about_window(self) -> None:
        mixer.Channel(0).play(mixer.Sound(SOUND_PATH + 'click.mp3'))
        self._about_window = BoggleAboutGui(self._opening)
        self._about_window.run()


if __name__ == '__main__':
    test = BoggleOpenGui()
    test.run()
