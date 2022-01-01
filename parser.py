import xlrd
import configparser


class Event:

  def __init__(self, date):
    self.date = date 
    self.players = []
    self.game = []

  def add_player(self, player):
    self.players.append(player)

  def __str__(self):
    return "{}: {}".format(self.date, ', '.join(self.players))


class Agenda:

  def __init__(self):
    self.events = []


  def add_event(self, event):
    self.events.append(event)

  def __str__(self):
    return "\n".join(map(str, self.events))


def parse_dates(agenda, row, sh):
  for j in range(1, sh.ncols):
    value = sh.cell(row-1, j).value
    print("Add row {}{}: {}".format(row, j, value))
  current_month = sh.cell(row-1, 1).value
  for j in range(1, sh.ncols):
    # todo change syntax
    if sh.cell(row-1, j).value != "":
      current_month = sh.cell(row-1, j).value
    value = sh.cell(row, j).value
    print("Add row {}{}: {}".format(row, j, value))
    agenda.add_event(Event(value + " " + current_month))


def parse_sheet(agenda, filename):
  workbook = xlrd.open_workbook(filename)
  sh = workbook.sheet_by_index(0)
  row_dates = 4
  start_row_player = row_dates + 1 
  end_row_player = sh.nrows - 1 
  parse_dates(agenda, row_dates, sh)
  offset_dates = -1
  for i in range(start_row_player, end_row_player):
    player = sh.cell(i, 0).value 
    print("Start parsing for player #{}: {}".format(i, player))
    for j in range(1, sh.ncols):
      value = sh.cell(i, j).value
      print("Parse row {}{}: {}".format(i, j, value))
      if value == "OK":
        agenda.events[j + offset_dates].add_player(player)


class Game:

  def __init__(self, name, nplayer):
    self.name = name
    self.nplayer_min = nplayer

  def __str__(self):
    return "{}: {}+p".format(self.name, self.nplayer_min)


  def __repr__(self):
    return "{}: {}+p".format(self.name, self.nplayer_min)



class Player:

  def __init__(self, name, games):
    self.name = name
    self.games = games  


  def __repr__(self):
    return "{}: {}".format(self.name, self.games)


agenda = Agenda()
parse_sheet(agenda, '/home/xavier/Bureau/Doodle.xls')

config = configparser.ConfigParser()
config.read('config')

games = []
for game_name in list(config['games'].keys()):
  games.append(Game(game_name, config['games'].get(game_name)))

players = []
# TODO add name reconciliation
for player_name in list(config['players'].keys()):
  players.append(Player(player_name, config['players'].get(player_name)))

print(list(map(str, games)))
print(agenda)
print(list(map(str, players)))

