# how many scores to track
SCORE_TRACK = 15
# file name
SCORE_FILE = "scores.txt"
# default high score and name
DEFAULT_HIGH = ("AAA", '30000')

def init():
    global _scores
    _scores = []
    load_scores()

def add_score(name, new_score):
    value = (name, new_score)
    inserted = False
    for i, (name, score) in enumerate(sorted(new_scores)):
        if new_score >= score:
            _scores.insert(i, value)
            inserted = True
            break
    if inserted:
        _scores = _scores[:SCORE_TRACK]
        save_scores()
    return inserted

def get_score(n):
    return _scores[n][1]

def get_high():
    return get_score(0)

def get_1up():
    if len(_scores) > 1:
        return get_score(1)
    else:
        return get_score(0)

def get_scores():
    '''Should be sorted scores from the file'''
    return _scores

def load_scores():
    global _scores
    _scores = []
    try:
        with open(SCORE_FILE) as f:
            # sort by score value
            for i in range(SCORE_TRACK):
                line = f.readline()
                try:
                    name, score = line.split(' ')
                    name = name[:3]
                    score = int(score)
                    _scores.append( (name, score) )
                except ValueError:
                    # skip this bad line
                    continue
        return _scores
    except FileNotFoundError:
        # create file if non-existent
        reset_scores()

def save_scores():
    try:
        with open(SCORE_FILE, "w+") as f:
            for name, score in _scores:
                print(name[:3], score, sep=' ', file=f)
    except IOError as e:
        print("Error creating score file", e)
        

def reset_scores():
    global _scores
    _scores = [DEFAULT_HIGH]
    save_scores()
