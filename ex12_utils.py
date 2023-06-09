from typing import List, Tuple
import boggle_board_randomizer

BOARD_SIZE = boggle_board_randomizer.BOARD_SIZE
BOARD_COORDINATES = [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE)]
DIRECTIONS = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
DIRECTIONS.remove((0, 0))


def convert_to_word(board: List[List[str]], path: List[Tuple[int, int]]) -> str:
    """
    This function convert list of tuple's that contains index to word.
    The function go over the board and the path simultaneously,
    and compare the index's of the board to data from the path.
    If there is a match the func chain the data from the board to our returned word.
    :param board: Board with letters, type List[List[str]].
    :param path: The word we search according to index's, type List[int].
    :return: The word we bring back, type str.
    """
    return ''.join(''.join([board[tup[0]][tup[1]] for tup in path]))


def is_valid_path(board: List[List[str]], path: List[Tuple[int, int]], words: any) -> any:
    """
    The function checks if the path is a valid path that describes a word that exists in the words dictinary.
    If so, the function returns the word found.
    If the path is invalid or the corresponding word does not exist in the dictionary, the function will return None.
    :param board: Board with letters, type List[List[str]].
    :param path: The word we search according to index's, type List[int].
    :param words: The dictinary of words, type any.
    :return: word or None, type str.
    """
    for tup in path:
        if tup[0] < 0 or tup[0] > 3 or tup[1] < 0 or tup[1] > 3:  # Check if out of boundaries.
            return None

        matrix = [(y, x) for y in range(tup[0] - 1, tup[0] + 2) for x in      # Some dynamic helper board.
                  range(tup[1] - 1, tup[1] + 2) if 0 <= y <= 3 and 0 <= x <= 3]
        next_index = path.index(tup) + 1

        if next_index < len(path):
            if path[next_index] not in matrix or path.count(tup) > 1:
                return None

    word = convert_to_word(board, path)
    if word not in set(words):
        return None

    return word


def find_length_n_helper(n: int, board: List[List[str]], words: any, directions: List[Tuple[int, int]],
                         list_of_paths: List[List[Tuple[int, int]]], path: List[Tuple[int, int]],
                         coordinate: Tuple[int, int], helper_for_words: bool, curr_word: str) -> List[List[Tuple[int, int]]]:
    """
    This function is helper for all the other functions.
    The function use backtracking and get all the possible words with length n.
    :param n: The length of the path, type int.
    :param board: Board with letters, type List[List[str]].
    :param words: Dictionary of all the valid words, type any.
    :param directions:
    :param list_of_paths:
    :param path:
    :param coordinate:
    :param helper_for_words:
    :param curr_word:
    :return:
    """
    if (len(path) >= n and not helper_for_words) or (len(curr_word) >= n and helper_for_words):
        word = convert_to_word(board, path)
        if word in words:
            list_of_paths.append(list(path))

        return list_of_paths

    for direction in directions:
        y = coordinate[0] + direction[0]
        x = coordinate[1] + direction[1]
        if (0 <= y <= 3 and 0 <= x <= 3) and (y, x) not in path:
            path.append((y, x))
            find_length_n_helper(n, board, words, directions, list_of_paths, path, (y, x), helper_for_words,
                                 curr_word + board[y][x])
            path.pop()

    return list_of_paths


def find_length_n_paths(n: int, board: List[List[str]], words: any) -> List[List[Tuple[int, int]]]:
    """
    The function returns a list of all n-length paths that describe words in the word dictionary.
    If there are several paths in length appropriate to the same word, all must be returned.
    The function use helper to do so.
    :param n: The length of the path, type int.
    :param board: Board with letters, type List[List[str]].
    :param words: Dictionary of all the valid words, type any.
    :return: List of paths, type List[List[Tuple[int]]].
    """
    paths = []
    if n == 0:
        return []

    for coordinate in BOARD_COORDINATES:
        paths.extend(find_length_n_helper(n, board, set(words), DIRECTIONS, [], [coordinate], coordinate, False,
                                          board[coordinate[0]][coordinate[1]]))

    return paths


def find_length_n_words(n: int, board: List[List[str]], words: any) -> List[List[Tuple[int, int]]]:
    """
    The function returns a list of all the paths that describe words in the dictionary of words that are of length n.
    If there are several paths to the same word, they must all be returned.
    :param n: The length of the path, type int.
    :param board: Board with letters, type List[List[str]].
    :param words: Dictionary of all the valid words, type any.
    :return: List of paths, type List[List[Tuple[int]]].
    """
    paths = []
    if n > 32 or n <= 0:
        return []

    filter_words = [word for word in words if len(word) == n]
    for coordinate in BOARD_COORDINATES:
        paths.extend(find_length_n_helper(n, board, set(filter_words), DIRECTIONS, [], [coordinate], coordinate, True,
                                          board[coordinate[0]][coordinate[1]]))

    return paths


def max_score_paths(board: List[List[str]], words: any) -> List[List[Tuple[int, int]]]:
    """
    The function returns a list of paths that provide the maximum score per game
    for the board and the dictionary of words given.
    :param board: Board with letters, type List[List[str]].
    :param words: Dictionary of all the valid words, type any.
    :return: List of paths, type List[List[Tuple[int]]].
    """

    longest_word_len = len(max(set(words), key=lambda w: len(w)))
    dict_of_words = dict()

    for n in range(1, longest_word_len + 1):
        paths = find_length_n_paths(n, board, set(words))
        for path in paths:
            word = convert_to_word(board, path)
            if word not in dict_of_words:
                dict_of_words[word] = [path]
            else:
                dict_of_words.setdefault(word, []).append(path)

    return [max(path, key=lambda pat: len(pat)) for path in dict_of_words.values()]
