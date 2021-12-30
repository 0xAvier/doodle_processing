import xlrd


def parse_dates(row, sh):
  res = []
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
    res.append([value + " " + current_month, []])
  return res


def parse_file(filename):
  workbook = xlrd.open_workbook(filename)
  sh = workbook.sheet_by_index(0)
  row_dates = 4
  start_row_player = row_dates + 1 
  end_row_player = sh.nrows - 1 
  dates = parse_dates(row_dates, sh)
  offset_dates = -1
  for i in range(start_row_player, end_row_player):
    player = sh.cell(i, 0).value 
    print("Start parsing for player #{}: {}".format(i, player))
    for j in range(1, sh.ncols):
      value = sh.cell(i, j).value
      print("Parse row {}{}: {}".format(i, j, value))
      if value == "OK":
        dates[j + offset_dates][1].append(player)

  print(dates)


    

parse_file('/home/xavier/Bureau/Doodle.xls')
