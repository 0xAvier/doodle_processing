class GameCollection:

    def __init__(self, games):
        self.games = games

    def find(self, name):
        try:
            game = next(
                filter(
                    lambda g: g.name.lower() == name.lower(),
                    self.games))
            return game
        except BaseException:
            names = ', '.join(self.names())
            print("Game '{}' not found in game list {}".format(name, names))
            raise

    def names(self):
        return [g.name for g in self.games]

    def __str__(self):
        return "\n".join(map(str, self.games))
