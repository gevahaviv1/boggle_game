from typing import List, Tuple
import ex12_utils
from pygame import mixer
WORDS_FILE = 'boggle_dict.txt'
SOUND_PATH = 'sounds/'


def load_words() -> set[str]:
    f = open(WORDS_FILE)
    text = set(line.strip() for line in f.readlines())
    f.close()
    return text


class BoggleModel:
    _board = List[str]
    _score: int
    _display_word: str
    _words_dict = dict()
    _exposed_words_dict: dict
    _words_dict: set[str]
    _exposed_words_display: str
    _path: List[Tuple[int, int]]

    def __init__(self) -> None:
        self._board = []
        self._score = 0
        self._words_found = []
        self._display_word = ''
        self._exposed_words_dict = {}
        self._words_dict = load_words()
        self._exposed_words_display = ''
        self._path = []

    def new_game(self) -> None:
        """
        The function set clear all for new game.
        :return: None.
        """
        self._board = []
        self._score = 0
        self._words_found = []
        self._display_word = ''
        self._exposed_words_dict = {}
        self._exposed_words_display = ''
        self._path = []

    def set_board(self, board: List[str]) -> None:
        """
        This function set the board game.
        :param board: The board, type List[str].
        :return: None.
        """
        self._board = board

    def get_score(self) -> int:
        """
        This function get the current score.
        :return: Score, type int.
        """
        return self._score

    def get_display_word(self) -> str:
        """
        This function get the current display word.
        :return: The current display word ,type str.
        """
        return self._display_word

    def get_exposed_words_display(self) -> str:
        """
        This function get the current exposed words.
        :return: The current exposed words ,type str.
        """
        return self._exposed_words_display

    def _do_clear(self) -> None:
        """
        This function clear the display word.
        :return: None.
        """
        self._display_word = ''
        self._path = []

    def _undo(self) -> None:
        """
        :return:
        """
        if self._display_word != '':
            self._display_word = str(self._display_word[:-1])
            self._path.pop()

    def _add_word(self):
        """
        This function add a word to the dictionary.
        :return: None.
        """
        if ex12_utils.is_valid_path(self._board, self._path, self._words_dict) and self._display_word not in\
                self._exposed_words_dict:
            self._exposed_words_display += '\n' + self._display_word
            self._exposed_words_dict[self._display_word] = True
            self._score += len(self._path)**2
            mixer.Channel(1).play(mixer.Sound(SOUND_PATH + 'add.mp3'))
            self._do_clear()

    def type_in(self, c: str, coordinate: Tuple[int, int]) -> None:
        """
        This function check what typed in from the user.
        :param c: What clicked, type str.
        :param coordinate: What coordinate, type Tuple[int, int].
        :return: None.
        """
        if c == 'Undo':
            self._undo()
        elif c == 'Clear':
            self._do_clear()
        elif c == 'Add':
            self._add_word()
        elif c.isalpha():
            self._path.append(coordinate)
            self._display_word += c
        else:
            raise ValueError("Unknown key")
        mixer.Channel(0).play(mixer.Sound(SOUND_PATH + 'click.mp3'))
