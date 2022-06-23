import csv
import subprocess


def read_games(game_line):
  return list(map(lambda s: s.replace(" ", ""), game_line))


def display_results(games, players, o_file):
  with open(o_file, 'w') as my_file:
    print_games(games, my_file)
    print_players(players, my_file)
    my_file.write("\n[options]\n")


def print_games(games, my_file):
  my_file.write("[games]\n")
  for g in games:
    if g != "":
      my_file.write(f"{g}=2-8\n")



def print_players(players, my_file):
  my_file.write("[players]\n")
  for key, value in players.items():
    my_file.write(f"{key}={','.join(value)}\n")


def generateConfigFromPoll(filename, o_file="output"):
  subprocess.call(["sed", "-i", "-e",  's/"//g', filename])
  players = {}
  with open(filename, newline='') as csvfile:
      sh = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
      n_row = len(list(sh))
      n_col = len(list(sh[0]))
      games = read_games(sh[0][1:])
      for i in range(1, n_row):
        player_name = sh[i][0]
        players[player_name] = []
        for j in range(1, n_col):
          if sh[i][j] == "Oui" or sh[i][j] == "Si nécessaire":
            players[player_name].append(games[j-1])
      display_results(games, players, o_file)
