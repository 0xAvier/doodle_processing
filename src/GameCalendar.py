import csv 
import re
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
        if len(sh[i]) == 0:
            continue
        date = sh[i][0] 
        for j in range(1, n_col):
          value = sh[i][j].split(':')
          if len(value) < 2:
            continue
          value = value[1]
          players = value.split(',')
          game = games[j-1]
          for p in players:
            p_key = p[1:]
            if self.players[p_key] is None:
              self.players[p_key] = []
            self.players[p_key].append([date, game])
          g_name = self._get_game_name_core(games[j-1], spaced=True)
          print(f"{date}: {g_name} avec{value}")


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


  def _format_date(self, date, time):
    s_date = date.split('/')
    res = f"{s_date[2]}-{s_date[1]}-{s_date[0]} {time}" 
    tz = 'Europe/Paris'
    return arrow.get(res, tzinfo=tz)

  def _parse_date(self, date, early_start):
    s_date = date.split('/')
    start_time = '19:00:00' if early_start else '19:30:00' 
    end_time = '23:00:00' 
    return self._format_date(date, start_time), self._format_date(date, end_time)


  # TODO
  # Move function to appropriate location (in Game.py?)
  def _get_game_name_core(self, name, spaced=False):
    res = name.split(' ')[0]
    if spaced:
      res = ' '.join(re.findall('[A-Z][^A-Z]*', res))
    return res 

  def write_calendars(self, configuration):
    for p in self.players.keys():
      c = ics.Calendar()
      gamenights = self.players[p]
      if gamenights is None:
        continue
      for gamenight in gamenights: 
        g_date = gamenight[0]
        g_name = self._get_game_name_core(gamenight[1])
        early_start = configuration.collection.find(g_name).early_start
        start, end = self._parse_date(g_date, early_start)
        e = ics.Event(name = g_name, begin = start, end=end)
        e.alarms = [
            ics.alarm.EmailAlarm(trigger=timedelta(days=-1)),
            ics.alarm.EmailAlarm(trigger=timedelta(minutes=-30))]
        c.events.add(e)
        if self.dates_per_game[g_name] is None:
          self.dates_per_game[g_name] = set() 
        self.dates_per_game[g_name].add(start)
      with open(f"{p}.ics", 'w') as my_file:
        my_file.writelines(c)
    self.display_stats(configuration)
