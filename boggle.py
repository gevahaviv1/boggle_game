from boggle_open_gui import BoggleOpenGui
from boggle_game_gui import BoggleGameGui
from boggle_model import BoggleModel
from typing import Callable, Tuple


class BoggleController:
    def __init__(self) -> None:
        self._game = None
        self._open_gui = BoggleOpenGui()
        self._model = BoggleModel()

    def run(self) -> None:
        self._open_gui.run()
        if self._open_gui.get_start():
            self.run_game()

    def run_game(self) -> None:
        self._game = BoggleGameGui()
        self._model.set_board(self._game.get_board())

        for btn in self._game.get_buttons():
            button_text = btn[0]
            button_coordinate = btn[2]
            action = self.create_button_action(button_text, button_coordinate)
            self._game.set_button_command(button_coordinate, action)
        self._game.set_display('')

        self._game.run()

        if self._game.get_tp_clicked():
            self._model.new_game()
            self.run_game()

    def create_button_action(self, button_text: str, button_coordinate: Tuple[int, int]) -> Callable[[], None]:
        def fun() -> None:
            self._model.type_in(button_text, button_coordinate)
            self._game.set_display(self._model.get_display_word())
            self._game.set_expose_words(self._model.get_exposed_words_display())
            self._game.set_score(self._model.get_score())
        return fun


if __name__ == '__main__':
    BoggleController().run()
