import configparser

from src.Game import Game
from src.GameCollection import GameCollection
from src.Player import Player
from src.Group import Group


class Configuration:

    def __init__(self, main_args):
        self.group = None
        self._parse_config(main_args.config, main_args.games_config)

    def _remove_impossible_games(self):
        m_player = self.group.mandatory_player()
        if not m_player:
            return
        mandatory_player_games = m_player.games
        initial_games = list(self.collection.games)
        for game in initial_games:
            if game not in mandatory_player_games:
                self.collection.remove_game(game.name)

    def _parse_config(self, config_fn, games_config_fn):
        games = []
        players = []

        config = configparser.ConfigParser(delimiters='=')
        config.optionxform = str
        config.read(config_fn)

        if games_config_fn is not None:
            games_config = configparser.ConfigParser(delimiters='=')
            games_config.optionxform = str
            games_config.read(games_config_fn)
            if 'games' in list(config.keys()):
                print(
                    "Warning: Games and options from global configuration file will be ignored")
        else:
            games_config = config

        for game_name in list(games_config['games'].keys()):
            game_config = games_config['games'].get(game_name)
            s_config = list(
                map(lambda s: s.strip(' '), game_config.split(';')))
            range_string = s_config[0]
            g = Game(game_name, range_string)
            for i in range(1, len(s_config)):
                g.add_option(s_config[i])
            games.append(g)

        self.collection = GameCollection(games)

        for player_name in list(config['players'].keys()):
            #  default games
            game_names = list(map(lambda s: s.strip(' '),
                                  config['players'].get(player_name).split(',')))
            pgames = list(map(lambda gn: self.collection.find(gn), game_names))
            #  under reserve games
            if 'players_under_reserve' in list(config.keys()):
                ur_game_names = list(map(lambda s: s.strip(
                    ' '), config['players_under_reserve'].get(player_name).split(',')))
                ur_game_names = filter(lambda s: len(s) > 0, ur_game_names)
                ur_pgames = list(
                    map(lambda gn: self.collection.find(gn), ur_game_names))
            else:
                ur_pgames = []
            players.append(Player(player_name, pgames, ur_pgames))

        if 'options' not in list(games_config.keys()):
            print("\n\n\n!!! Warning: no options provided !!!\n\n")
            if games_config_fn is not None and 'options' in list(
                    config.keys()):
                print(
                    "!!! Options provided in global configuration file are ignored if game configuration file is used !!!\n\n")
            nbhosts = 0
            mandatory_name = None
            hosts = []
        else:
            options_config = games_config['options']

            nhosts = int(options_config['nhosts']
                         ) if 'nhosts' in options_config.keys() else 0
            mandatory_name = options_config['mandatory_player'] if 'mandatory_player' in options_config.keys(
            ) else None
            hosts = []
            for nhost in range(nhosts):
                hosts.append(Player("host_{}".format(nhost + 1), games))

        self.group = Group(
            players,
            hosts,
            mandatory_player_name=mandatory_name)
        self._remove_impossible_games()
