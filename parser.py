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


def parse_file(agenda, filename):
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


agenda = Agenda()
parse_file(agenda, '/home/xavier/Bureau/Doodle.xls')

