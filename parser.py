import xlrd
import configparser


class Game:

  def __init__(self, name, nplayer):
    self.name = name
    self.nplayer_min = nplayer

  def __str__(self):
    return "{}: {}+p".format(self.name, self.nplayer_min)


  def __repr__(self):
    return "{}: ({}+p)".format(self.name, self.nplayer_min)


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
    # TODO: put min player / max player
    games.append(Game(game_name, int(config['games'].get(game_name))))

  collection = GameCollection(games)
  
  for player_name in list(config['players'].keys()):
    game_names = config['players'].get(player_name).split(', ')
    pgames = list(map(lambda gn: collection.find(gn), game_names))
    players.append(Player(player_name, pgames))


  nhosts = int(config['options']['host']) if 'host' in config['options'].keys() else 0;
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
    return [[g, self.games_dict[g]] for g in self.games_dict.keys() if len(self.games_dict[g]) >= g.nplayer_min]


  def str_full_games(self):
    disp = lambda e: "{} {}p ({})".format(e[0].name, len(e[1]), ', '.join(e[1]))
    return ';'.join(list(map(disp, self.full_games())))


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


  def _parse_dates(self, row, sh):
    for j in range(1, sh.ncols):
      value = sh.cell(row-1, j).value
    current_month = sh.cell(row-1, 1).value
    for j in range(1, sh.ncols):
      if (v := sh.cell(row-1, j).value) != "":
        current_month = v
      value = sh.cell(row, j).value
      self.add_event(Event(value + " " + current_month))


def find_matches(agenda, collection, group):
  for e in agenda.events:
    for p in e.players:
      player = group.find(p)
      e.add_game_for_player(player)
    e.add_hosts(group.hosts)


group, collection = parse_config('config')
agenda = Agenda('/home/xavier/Bureau/Doodle.xls')
find_matches(agenda, collection, group)
# TODO: translate date
print(agenda)
