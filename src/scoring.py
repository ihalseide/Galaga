# how many scores to track
SCORE_TRACK = 15
# file name
SCORE_FILE = "scores.txt"
# default high score and name
DEFAULT_HIGH = ("AAA", '30000')

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
        scores = []
        with open(SCORE_FILE) as f:
            # sort by score value
            for i in range(SCORE_TRACK):
                line = f.readline()
                try:
                    name, score = line.split(' ')
                    name = name[:3]
                    score = int(score)
                    scores.append( (name, score) )
                except ValueError:
                    # skip this bad line
                    continue
        return scores
    except IOError:
        if second_try:
            return None
        else:
            reset_scores()
            return get_scores(second_try=True)

def reset_scores():
    try:
        # create file if non-existent
        with open(SCORE_FILE, "w+") as f:
            f.write(' '.join(DEFAULT_HIGH))
    except IOError as e:
        print("Error creating score file", e)
