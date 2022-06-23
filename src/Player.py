class Player:

    def __init__(self, name, games):
        self.name = name
        self.games = games

    def __repr__(self):
        return "{}: {}".format(self.name, self.games)
