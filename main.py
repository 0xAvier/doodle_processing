import configparser
import argparse

from src.Game import Game 
from src.GameCollection import GameCollection
from src.Player import Player 
from src.Group import Group 
from src.Agenda import Agenda 


def parse_config(filename):
  games = []
  players = []

  config = configparser.ConfigParser()
  config.optionxform = str
  config.read(filename)

  for game_name in list(config['games'].keys()):
    range_string = config['games'].get(game_name)
    games.append(Game(game_name, range_string))

  collection = GameCollection(games)
  
  for player_name in list(config['players'].keys()):
    game_names = config['players'].get(player_name).split(', ')
    pgames = list(map(lambda gn: collection.find(gn), game_names))
    players.append(Player(player_name, pgames))


  nhosts = int(config['options']['nhosts']) if 'nhosts' in config['options'].keys() else 0;
  hosts = []
  for nhost in range(nhosts):
    hosts.append(Player("host_{}".format(nhost+1), games))

  group = Group(players, hosts)
  return group, collection


def find_matches(agenda, collection, group):
  for e in agenda.events:
    for p in e.players:
      player = group.find(p)
      e.add_game_for_player(player)
    e.add_hosts(group.hosts)



parser = argparse.ArgumentParser(description='Find matching')
parser.add_argument('-s', '--sheet', required=True)
parser.add_argument('--config', default='config')
args = parser.parse_args()

# TODO move parse config out of main
# TODO refactor the matching part
# TODO do the per game column
# TODO do the stats per player per game
group, collection = parse_config(args.config)
agenda = Agenda(args.sheet)
find_matches(agenda, collection, group)
print(agenda)
