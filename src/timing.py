class Ticker(object):
    def __init__(self, delay=1):
        self.time = 0
        self.delay = delay

    def update(self, delta_time):
        """
        Try to tick and return whether it did
        """
        self.time += delta_time
        if self.time >= self.delay:
            self.time = 0
            return True
        else:
            return False

class ToggleTicker(object):
    def __init__(self, period=1, start_on=True):
        self.time = 0
        self.period = period
        self.on = start_on

    def update(self, delta_time):
        """
        Return whether the state changed also
        """
        self.time += delta_time
        if self.time >= self.period:
            self.time = 0
            self.on = not self.on
            return True
        else:
            return False

class Countdown(object):
    def __init__(self, time=1):
        self.time = time
        self.done = False

    def update(self, delta_time):
        """
        Return True if the countdown is finished, False otherwise
        """
        if self.time <= 0:
            self.done = True
        else:
            self.time -= delta_time
            self.done = False
        return self.done
