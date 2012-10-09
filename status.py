__all__ = ['status']

class Status():
    def __init__(self):

        # current level object
        self.level = None

        # current level id
        self.level_id = 0

        # dudes blowed up
        self.kills = 0


    def reset(self):
        self.level = None
        self.level_id = 0
        self.kills = 0

status = Status()
