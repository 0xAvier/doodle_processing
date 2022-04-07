import csv
from datetime import datetime
from src.Event import Event
import subprocess

class Agenda:

  def __init__(self, sheetname):
    self.events = []
    self._parse_sheet(sheetname)


  def add_event(self, event):
    self.events.append(event)


  def __str__(self):
    return "\n".join(map(str, self.events))


  def _parse_sheet(self, filename):
    subprocess.call(["sed", "-i", "-e",  's/"//g', filename])
    with open(filename, newline='') as csvfile:
      sh = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
      n_row = len(list(sh))
      n_col = len(list(sh[0]))
      row_dates = 0
      column_offset_events = 1
      start_row_player = row_dates + 2
      end_row_player = n_row 
      self._parse_dates(row_dates, sh)
      for i in range(start_row_player, end_row_player):
        player = sh[i][0]
        for j in range(1, n_col):
          value = sh[i][j]
          if value == "Oui":
            self.events[j-column_offset_events].add_player(player)


  def _parse_dates(self, row, sh):
    for j in range(1, len(sh[0])):
      value = sh[row][j]
      if len(value) > 0:
        self.add_event(Event(value))


  def find_matches(self, configuration):
    for e in self.events:
      for p in e.players:
        player = configuration.group.find(p)
        e.add_game_for_player(player)
      e.add_hosts(configuration.group.hosts)


  def _display_csv_header(games):
    print(";", end='')
    for g in games:
      print("{} {}p;".format(g.name, g.nplayers_str), end='')
    print("")


  def _display_blank_line(configuration):
    print(';'.join(['' for _ in range(len(configuration.collection.games) + 1)]))


  def sort_games(games, events, mandatory_player_name):
    total = []
    for event in events:
      if mandatory_player_name is not None and \
          not event.has_player(mandatory_player_name):
        continue
      total+= map(lambda g: g[0].name, event.full_games())
    res = sorted(games, key=lambda g: total.count(g.name), reverse=True)
    res = filter(lambda g: total.count(g.name) > 0, res)
    return list(res)


  def display_csv(self, configuration):
    mandatory_player_name = configuration.group.mandatory_player_name
    sorted_games = Agenda.sort_games(configuration.collection.games, self.events, mandatory_player_name)
    Agenda._display_csv_header(sorted_games)
    # TODO order games by nplayers
    for event in self.events:
      if datetime(event.year(), event.month(), event.day()).weekday() == 0:
        print("")
      print("{};".format(event.date), end='')
      if mandatory_player_name is not None and \
        not event.has_player(mandatory_player_name):
        Agenda._display_blank_line(configuration)
        continue
      full_games = event.full_games()
      for g in sorted_games: 
        # TODO with refactor matching
        matching = list(filter(lambda m: m[0].name.lower() == g.name.lower(),
          full_games))
        if len(matching) == 1:
          nplayers = g.nplayer_str(len(matching[0][1]))
          players = ', '.join(matching[0][1])
          print("{}: {};".format(nplayers, players), end='')
        else:
          print(";", end='')
      print("")


