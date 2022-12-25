class Group:

    def __init__(self, players, hosts, mandatory_player_name=None):
        self.players = players
        self.hosts = hosts
        self.mandatory_player_name = mandatory_player_name

    def find(self, name):
        try:
            player = next(
                filter(
                    lambda p: p.name.lower() == name.lower(),
                    self.players))
            return player
        except BaseException:
            names = ', '.join(self.names())
            print("Player {} not found in player list {}".format(name, names))
            raise

    def contains_mandatory_player(self, players):
        print(list(map(lambda p: p.name, players)))
        print(self.mandatory_player_name in map(lambda p: p.name, players))
        return self.mandatory_player_name in map(lambda p: p.name, players)

    def mandatory_player(self):
        if self.mandatory_player_name:
            return self.find(self.mandatory_player_name)
        return None

    def names(self):
        return [p.name for p in self.players]

    def __str__(self):
        return "\n".join(map(str, self.players))
