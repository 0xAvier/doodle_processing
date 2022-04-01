import csv
import arrow
import ics 
from datetime import timedelta, timezone


class GameCalendar:


  def __init__(self, sheetname, configuration):
    keys = map(lambda p: p.name, configuration.group.players + configuration.group.hosts)
    self.players = dict.fromkeys(keys)
    keys = map(lambda g: g.name, configuration.collection.games)
    self.dates_per_game = dict.fromkeys(keys)
    self._parse_sheet(sheetname)


  def _parse_game_line(self, sh):
    game_line = 0
    row_start = 1
    n_col = len(list(sh[game_line]))
    games = [None for i in range(n_col-1)]
    for i in range(n_col-row_start):
      games[i] = sh[game_line][i+row_start]

    return games

      

  def _parse_sheet(self, filename):
    with open(filename, newline='') as csvfile:
      sh = list(csv.reader(csvfile, delimiter=';', quotechar='"'))
      n_row = len(list(sh))
      n_col = len(list(sh[0]))

      games = self._parse_game_line(sh)

      row_dates = 1
      for i in range(row_dates, n_row):
        date = sh[i][0] 
        for j in range(1, n_col):
          value = sh[i][j].split(':')
          if len(value) < 2:
            continue
          value = value[1]
          players = value.split(',')
          for p in players:
            p_key = p[1:]
            if self.players[p_key] is None:
              self.players[p_key] = []
            self.players[p_key].append([date, games[j-1]])


  def display_stats(self, configuration):
    values = []
    for p in self.players.keys():
      events = self.players[p]
      if events is None:
        events = []
      values.append([p, len(events)])
    sorted_values = sorted(values, key=lambda e: e[1], reverse=True)
    for p in sorted_values:
      print(f"{p[0]} will play {p[1]} times")

    print("-----")
    values = []
    for g in self.dates_per_game.keys():
      events = self.dates_per_game[g]
      if events is None:
        events = []
      values.append([g, len(events)])
    sorted_values = sorted(values, key=lambda e: e[1], reverse=True)
    for g in sorted_values:
      print(f"{g[0]} will be played {g[1]} times")


  def _parse_date(self, date, early_start):
    s_date = date.split('/')
    start_time = '19:00:00' if early_start else '19:30:00' 
    res = f"{s_date[2]}-{s_date[1]}-{s_date[0]} {start_time}" 
    tz = 'Europe/Paris'
    return arrow.get(res, tzinfo=tz)

  def write_calendars(self, configuration):
    for p in self.players.keys():
      c = ics.Calendar()
      gamenights = self.players[p]
      if gamenights is None:
        continue
      for gamenight in gamenights: 
        g_name = gamenight[1].split(' ')[0]
        early_start = configuration.collection.find(g_name).early_start()
        g_date = self._parse_date(gamenight[0], early_start)
        e = ics.Event()
        e.begin = g_date
        e.name = g_name 
        e.alarms = [
            ics.alarm.EmailAlarm(trigger=timedelta(days=-1)),
            ics.alarm.EmailAlarm(trigger=timedelta(minutes=-30))]
        c.events.add(e)
        if self.dates_per_game[g_name] is None:
          self.dates_per_game[g_name] = set() 
        self.dates_per_game[g_name].add(g_date)
      with open(f"{p}.ics", 'w') as my_file:
        my_file.writelines(c)
    self.display_stats(configuration)
