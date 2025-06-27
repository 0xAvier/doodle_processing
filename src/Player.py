class Player:

    def __init__(self, name, games, ur_games):
        self.name = name
        self.games = games
        self.under_reserve_games = ur_games

    def __repr__(self):
        return "{}: {}".format(self.name, self.games, self.under_reserve_games)
