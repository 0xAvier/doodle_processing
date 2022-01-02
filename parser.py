import xlrd
import configparser
import argparse


class Game:

  def __init__(self, name, ranges):
    self.name = name
    self.nplayers = []
    self._parse_nplayer_range(ranges)

  def _parse_nplayer_range(self, string):
      ranges = string.split(',') 
      for r in ranges:
        subr = r.split('-')
        if len(subr) == 1:
          self.nplayers.append(int(subr[0]))
        elif len(subr) == 2:
          self.nplayers += range(int(subr[0]), int(subr[1]) + 1)
        else:
          raise Exception("A range should be either 'a' or 'a-b', chained by ','. {} is incorrect".format(string))


  def nplayer_max(self):
    return self.nplayers[-1]


  # TODO check str vs repr
  def __str__(self):
    return "{}: ({}p)".format(self.name, "/".join(self.nplayers))


  def __repr__(self):
    return "{}: ({}p)".format(self.name, "/".join(self.nplayers))


class GameCollection:

  def __init__(self, games):
    self.games = games


  def find(self, name):
    try:
      game = next(filter(lambda g: g.name.lower() == name.lower(), self.games))
      return game
    except:
      names = ', '.join(self.names())
      print("Game '{}' not found in game list {}".format(name, names))
      raise


  def names(self):
    return [g.name for g in self.games]


  def __str__(self):
    return "\n".join(map(str, self.games))


class Player:

  def __init__(self, name, games):
    self.name = name
    self.games = games  


  def __repr__(self):
    return "{}: {}".format(self.name, self.games)


class Group:

  def __init__(self, players, hosts):
    self.players = players 
    self.hosts = hosts


  def find(self, name):
    try:
      player = next(filter(lambda p: p.name.lower() == name.lower(), self.players))
      return player
    except:
      names = ', '.join(self.names())
      print("Player {} not found in player list {}".format(name, names))
      raise


  def names(self):
    return [p.name for p in self.players]


  def __str__(self):
    return "\n".join(map(str, self.players))



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


class Event:

  def __init__(self, date):
    self.date = date 
    self.players = []
    self.games_dict = {}

  def add_player(self, player):
    self.players.append(player)


  def full_games(self):
    return [[g, self.games_dict[g]] for g in self.games_dict.keys() if len(self.games_dict[g]) in g.nplayers]


  def _format_full_game(full_game):
    g = full_game[0]
    players = full_game[1]
    pnames = ', '.join(players)
    if g.nplayer_max() < len(players):
      nplayers = "{}/{}p".format(g.nplayer_max, len(players))
    else:
      nplayers = "{}p".format(len(players))
    disp = lambda e: "{} {} ({})".format(g.name, nplayers, pnames) 
    return disp(full_game)

  def str_full_games(self):
    return ';'.join(list(map(Event._format_full_game, self.full_games())))


  def add_game_for_player(self, player):
    for g in player.games:
      if g not in self.games_dict:
        self.games_dict[g] = []
      self.games_dict[g].append(player.name)


  def add_hosts(self, hosts):
    for g in self.games_dict.keys(): 
      for h in hosts:
        self.games_dict[g].append(h.name)


  def __str__(self):
    return "{};{}".format(self.date, self.str_full_games())


class Agenda:

  def __init__(self, sheetname):
    self.events = []
    self._parse_sheet(sheetname)


  def add_event(self, event):
    self.events.append(event)


  def __str__(self):
    return "\n".join(map(str, self.events))


  def _parse_sheet(self, filename):
    workbook = xlrd.open_workbook(filename)
    sh = workbook.sheet_by_index(0)
    row_dates = 4
    start_row_player = row_dates + 1 
    end_row_player = sh.nrows - 1 
    self._parse_dates(row_dates, sh)
    offset_dates = -1
    for i in range(start_row_player, end_row_player):
      player = sh.cell(i, 0).value
      for j in range(1, sh.ncols):
        value = sh.cell(i, j).value
        if value == "OK":
          self.events[j + offset_dates].add_player(player)

  def translate_month(self, date):
    month_dict = {
      "January": "Jan.", 
      "February": "Fév.", 
      "March": "Mars", 
      "April": "Avr.", 
      "May": "Mai", 
      "June": "Juin", 
      "July": "Juil.", 
      "August": "Août", 
      "September": "Sept.", 
      "October": "Oct.", 
      "November": "Nov.", 
      "December": "Déc."
    }
    res = date 
    for m in month_dict.keys():
      res = res.replace(m, month_dict[m])
    return res 


  def translate_day(self, date):
    day_dict = {
      "Mon": "Lun.", 
      "Tue": "Mar.", 
      "Wed": "Mer.", 
      "Thu": "Jeu.", 
      "Fri": "Ven.", 
      "Sat": "Sam.", 
      "Sun": "Dim."
    }
    res = date 
    for d in day_dict.keys():
      res = res.replace(d, day_dict[d])
    return res 


  def _parse_dates(self, row, sh):
    for j in range(1, sh.ncols):
      value = sh.cell(row-1, j).value
    current_month = self.translate_month(sh.cell(row-1, 1).value)
    for j in range(1, sh.ncols):
      if (v := sh.cell(row-1, j).value) != "":
        current_month = self.translate_month(v)
      value = self.translate_day(sh.cell(row, j).value)
      self.add_event(Event(value + " " + current_month))


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

group, collection = parse_config(args.config)
agenda = Agenda(args.sheet)
find_matches(agenda, collection, group)
print(agenda)
