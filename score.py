import json

SCORE_TRACK = 15
SCORE_FILE = "highscores.json"
DEFAULT_HIGH = ("AAA", 30000)

def add_score(name, score):
    value = name, score
    scores = get_scores()
    new_scores = scores.copy()
    inserted = False
    for i, scr in enumerate(sorted(new_scores)):
        if score >= scr[1]:
            new_scores.insert(i, value)
            inserted = True
            break
    if inserted:
        new_scores = new_scores[:SCORE_TRACK]
        with open(SCORE_FILE, "w+") as f:
            json.dump(new_scores, f)
    return inserted

def get_highscore():
    s = get_scores()
    if s:
        return s[0]
    else:
        return None

def get_scores(second_try=False):
    try:
        with open(SCORE_FILE) as f:
            # sort by score value
            return sorted(json.load(f), key=lambda x: x[1])
    except IOError:
        if second_try:
            return None
        else:
            reset_scores()
            return get_scores(second_try=True)

def reset_scores():
    # create file if non-existent
    with open(SCORE_FILE, "w+") as f:
        json.dump([DEFAULT_HIGH], f)
