import configparser

from src.Game import Game
from src.GameCollection import GameCollection
from src.Player import Player
from src.Group import Group

class Configuration:

  def __init__(self, config_fn):
    self._parse_config(config_fn)

  def _parse_config(self, filename):
    games = []
    players = []

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(filename)

    for game_name in list(config['games'].keys()):
      game_config = config['games'].get(game_name)
      s_config = game_config.split('; ')
      range_string = s_config[0] 
      g = Game(game_name, range_string)
      for i in range(1, len(s_config)):
        g.add_option(s_config[i])
      games.append(g)

    self.collection = GameCollection(games)

    for player_name in list(config['players'].keys()):
      game_names = config['players'].get(player_name).split(', ')
      pgames = list(map(lambda gn: self.collection.find(gn), game_names))
      players.append(Player(player_name, pgames))


    nhosts = int(config['options']['nhosts']) if 'nhosts' in config['options'].keys() else 0;
    hosts = []
    for nhost in range(nhosts):
      hosts.append(Player("host_{}".format(nhost+1), games))

    self.group = Group(players, hosts)


