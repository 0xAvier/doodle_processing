import sys


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
            sys.stderr.write(
                "Game '{}' not found in game list {}\n".format(name, names))
            raise

    def names(self):
        return [g.name for g in self.games]

    def remove_game(self, game_name):
        self.games.remove(self.find(game_name))

    def __str__(self):
        return "\n".join(map(str, self.games))
