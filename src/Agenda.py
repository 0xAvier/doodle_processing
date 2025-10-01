import csv
import sys
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
        if filename is None:
            print("No sheet file name given. Abort.")
            sys.exit()
        subprocess.call(["sed", "-i", "-e", 's/"//g', filename])
        with open(filename, newline="", mode='r') as csvfile:
            nb_yes = 0
            sh = list(csv.reader(csvfile, delimiter=",", quotechar='"'))
            n_row = len(list(sh))
            n_col = len(list(sh[0]))
            if n_row < 2:
                raise Exception(
                    f"Not enough row found ({n_row}) check the csv file delimiter")
            if n_col < 2:
                raise Exception(
                    f"Not enough column found ({n_col}), check the csv file delimiter")
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
                        nb_yes += 1
                        self.events[j -
                                    column_offset_events].add_player(player)
                    if value == "Si nécessaire":
                        nb_yes += 1
                        self.events[j -
                                    column_offset_events].add_player_under_reserve(player)
            if nb_yes == 0:
                raise Exception(
                    "No 'Oui' found, have you given the right sheet?")

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
            for p in e.players_under_reserve:
                player = configuration.group.find(p)
                e.add_game_for_player_under_reserve(player)
            e.add_hosts(configuration.group.hosts)

    def _display_csv_header(self, games, mandatory_player_name):
        print(";", end="")
        matches_per_game = Agenda.matches_per_game(
            games, self.events, mandatory_player_name
        )
        for g in games:
            print(
                "{} {} matches;".format(
                    g.name.replace("_", " "), matches_per_game[g.name]
                ),
                end="",
            )
        print("")

    def _display_blank_line(configuration):
        print(
            ";".join(["" for _ in range(len(configuration.collection.games) + 1)]))

    def matches_per_game(games, events, mandatory_player_name):
        res = {}
        for event in events:
            if mandatory_player_name is not None and not event.has_player(
                mandatory_player_name
            ):
                continue
            for g in event.full_games():
                n = g[0].name
                if n not in res:
                    res[n] = 0
                res[g[0].name] += 1

        return res

    def sort_games(games, events, mandatory_player_name):
        total = []
        for event in events:
            if mandatory_player_name is not None and not event.has_player(
                mandatory_player_name
            ):
                continue
            total += map(lambda g: g[0].name, event.full_games())
        res = sorted(games, key=lambda g: total.count(g.name))
        res = filter(lambda g: total.count(g.name) > 0, res)
        return list(res)

    def display_csv(self, configuration):
        mandatory_player_name = configuration.group.mandatory_player_name
        sorted_games = Agenda.sort_games(
            configuration.collection.games, self.events, mandatory_player_name
        )
        self._display_csv_header(sorted_games, mandatory_player_name)
        for event in self.events:
            if datetime(
                    event.year(),
                    event.month(),
                    event.day()).weekday() == 0:
                print("")
            print("{};".format(event.date), end="")
            if mandatory_player_name is not None and not event.has_player(
                mandatory_player_name
            ):
                Agenda._display_blank_line(configuration)
                continue
            full_games = event.full_games()
            for g in sorted_games:
                # TODO with refactor matching
                matching = list(
                    filter(
                        lambda m: m[0].name.lower() == g.name.lower(),
                        full_games))
                # TODO Need to refactor this matching with a decent object: accessing [0][1] to get info is not OK 
                if len(matching) == 0 or (
                        mandatory_player_name and mandatory_player_name not in matching[0][1]['default'] and mandatory_player_name not in matching[0][1]['under_reserve']):
                    print(";", end="")
                else:
                    nplayers = len(
                        matching[0][1]['default'] +
                        matching[0][1]['under_reserve'])
                    nplayers_str = g.nplayer_str(nplayers)
                    players = ", ".join(matching[0][1]['default'])
                    under_reserve_players = ", ".join(
                        matching[0][1]['under_reserve'])
                    res = "{}: ".format(nplayers_str)
                    if len(players):
                        res += "{}".format(players)
                    if len(under_reserve_players):
                        if len(players):
                            res += ", "
                        res += "({})".format(under_reserve_players)
                    res += ";"
                    print(res, end='')
            print("")
