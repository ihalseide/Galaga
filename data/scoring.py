#!/usr/bin/env python3

# scoring.py


from collections import namedtuple

from . import constants as c


# how many scores to track
SCORES_LENGTH = 15
# file name
# default high score and name
DEFAULT_HIGH = ("AAA", '30000')

Score = namedtuple('Score', 'name score')

# Where the scores are stored for the game
_scores = None


def get_high_score() -> int:
    # TODO: return the current high score in the list
    pass


def get_1up_score() -> int:
    # TODO: return what score is needed to get the next 1UP
    pass


def is_higher_score(compare_score: int) -> bool:
    # TODO: return if the passed score is bigger than the current hi-score
    pass


def add_score(name: str, score: int):
    # TODO: add a score to the list in the right spot, while maintaining the right length
    pass


def clear_scores():
    global _scores
    _scores = []


def load_scores() -> list:
    global _scores
    scores = []
    with open(c.SCORE_FILE) as file:
        for line in file.readlines():
            name, score = line.split(' ')
            score = int(score)
            score_tuple = Score(name, score)
            scores.append(score_tuple)
    _scores = scores
    return _scores


def save_scores():
    global _scores
    lines = ["{} {}".format(name, score) for (name, score) in _scores]
    with open(c.SCORE_FILE) as file:
        file.writelines(lines)


def init():
    clear_scores()
    load_scores()