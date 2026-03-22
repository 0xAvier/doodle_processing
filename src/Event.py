class Event:

    def __init__(self, date):
        self.date = date
        self.players = []
        self.players_under_reserve = []
        # TODO here replace games_dict with new class object 'matching'
        self.games_dict = {}

    def add_player(self, player):
        self.players.append(player)

    def add_player_under_reserve(self, player):
        self.players_under_reserve.append(player)

    def has_player(self, player_name):
        return player_name in self.players

    def full_games(self):
        def owner_there(g): return g.owner_name is None or self.has_player(
            g.owner_name)

        # Number of confirmed players for a game
        def nb_default(g): return len(self.games_dict[g]['default'])
        # Number of confirmed + under-reserve players for a game

        def nb_total(g): return nb_default(g) + len(
            self.games_dict[g]['under_reserve'])
        # Whether confirmed players alone meet the game's player count

        def enough_default(g): return nb_default(
            g) in g.nplayers or nb_default(g) > g.nplayer_min()
        # Whether confirmed + under-reserve players meet the game's player
        # count
        def enough_with_reserve(g): return nb_total(
            g) in g.nplayers or nb_total(g) > g.nplayer_min()

        result = []
        for g in self.games_dict.keys():
            if not owner_there(g):
                continue
            if not enough_with_reserve(g):
                continue
            # Include under-reserve players only if the game isn't
            # already full with confirmed players alone
            if nb_default(g) >= g.nplayer_max():
                result.append([g, {'default': self.games_dict[g]['default'],
                                   'under_reserve': []}])
            else:
                result.append([g, self.games_dict[g]])
        return result

    def _format_full_game(full_game):
        g = full_game[0]
        players = full_game[1]['default']
        urplayers = full_game[1]['under_reserve']
        pnames = ', '.join(players)
        urpnames = ', '.join(urplayers)
        nplayer = len(players) + len(urplayers)
        if nplayer in g.nplayers:
            nplayers = "{}p".format(nplayer)
        elif g.nplayer_max() < nplayer:
            nplayers = "{}/{}p".format(g.nplayer_max(), nplayer)
        elif nplayer not in g.nplayers:
            nplayers = "{}/{}p".format(
                g.nplayer_smallest_max(nplayer), nplayer)
        else:
            raise Exception("Full game error")

        def disp(e): return "{} {} ({}, ({}))".format(
            g.name, nplayers, pnames, urpnames)
        return disp(full_game)

    def year(self):
        if (len(self.date) < 8):
            return None
        return int(self.date[0:4])
        print(self.date)
        # TODO find good format
        return int(self.date[6:10])

    def month(self):
        if (len(self.date) < 8):
            return None
        return int(self.date[5:7])
        return int(self.date[3:5])

    def day(self):
        if (len(self.date) < 8):
            return None
        return int(self.date[8:10])
        return int(self.date[0:2])

    def str_full_games(self):
        return ';'.join(list(map(Event._format_full_game, self.full_games())))

    def add_game_for_player(self, player):
        for g in player.games:
            if g not in self.games_dict:
                self.games_dict[g] = {'default': [], 'under_reserve': []}
            self.games_dict[g]['default'].append(player.name)
        for g in player.under_reserve_games:
            if g not in self.games_dict:
                self.games_dict[g] = {'default': [], 'under_reserve': []}
            self.games_dict[g]['under_reserve'].append(player.name)

    def add_game_for_player_under_reserve(self, player):
        for g in player.games:
            if g not in self.games_dict:
                self.games_dict[g] = {'default': [], 'under_reserve': []}
            self.games_dict[g]['under_reserve'].append(player.name)
        for g in player.under_reserve_games:
            if g not in self.games_dict:
                self.games_dict[g] = {'default': [], 'under_reserve': []}
            self.games_dict[g]['under_reserve'].append(player.name)

    def add_hosts(self, hosts):
        for g in self.games_dict.keys():
            for h in hosts:
                self.games_dict[g].append(h.name)

    def __str__(self):
        return "{};{}".format(self.date, self.str_full_games())
