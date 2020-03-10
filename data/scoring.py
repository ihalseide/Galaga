# This scoring module is not a class because it is meant to be more of a singleton

from . import constants as c
from collections import namedtuple

Score = namedtuple('Score', 'name score')

# default high score and name
DEFAULT_HIGH = Score("AAA", '30000')

# Where the scores are stored for the game
SCORES_LENGTH = 5  # how many scores to keep track of
_scores: list = []  # scores list


def get_high_score(current_score: int = 0) -> int:
	# return the current high score in the list
	global _scores
	max_in_record = max(_scores, key=lambda score: score.score).score
	if current_score:
		return max(max_in_record, current_score)
	else:
		return max_in_record


def get_1up_score() -> int:
	# TODO: return what score is needed to get the next 1UP
	return 0


def is_highest_score(compare_score: int) -> bool:
	# return if the passed score is bigger than the current hi-score
	global _scores
	for (_, old_score) in _scores:
		if compare_score < old_score:
			return False
	return True


def add_score(name: str, score: int):
	global _scores
	_scores.append(Score(name, score))
	_scores = list(reversed(sorted(_scores, key=lambda s: s.score)))
	_scores = _scores[:SCORES_LENGTH]  # only take so many scores by trimming off any extra


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
	lines = ["{} {}".format(name, score) for (name, score) in _scores[:SCORES_LENGTH]]
	with open(c.SCORE_FILE) as file:
		file.writelines(lines)


load_scores()
