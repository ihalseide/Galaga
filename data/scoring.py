from collections import namedtuple

from . import constants as c

ScoreRecord = namedtuple('Score', 'name score')

NUM_TRACKED_SCORES = c.NUM_TRACKED_SCORES


def load_scores() -> list:
    scores = []
    with open(c.SCORE_FILE) as file:
        # Read a max of NUM_TRACKED_SCORES lines
        for line, _ in zip(file, range(NUM_TRACKED_SCORES)):
            try:
                name, score = line.split(' ')
                name = name[:3]  # Limit name length to 3
                score = int(score)  # The score is an int.
                record = ScoreRecord(name, score)
                scores.append(record)
            except ValueError as e:
                print("[Warning]: ValueError caught in loading scores -", e)
    if not scores:
        return [ScoreRecord('AAA', 30_000),
                ScoreRecord('BBB', 20_000),
                ScoreRecord('CCC', 10_000),
                ScoreRecord('DDD', 9_000),
                ScoreRecord('EEE', 8_000)]
    return scores


def save_scores(scores):
    sorted_scores = sorted(scores)
    lines = ["{} {}".format(record.name, record.score) for record in sorted_scores[:NUM_TRACKED_SCORES]]
    with open(c.SCORE_FILE) as file:
        file.writelines(lines)
