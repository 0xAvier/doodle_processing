#!/usr/bin/env python3
import argparse

from src.Configuration import Configuration
from src.ConfigFromPoll import generateConfigFromPoll
from src.Agenda import Agenda
from src.GameCalendar import GameCalendar


def parse_args():
    parser = argparse.ArgumentParser(description='Find matching')
    parser.add_argument('-s', '--sheet')
    parser.add_argument('-c', '--config', default='config')
    parser.add_argument('-g', '--games', default=None, dest='games_config')
    parser.add_argument('-o', '--output', default='ouput')
    parser.add_argument(
        '-i',
        '--create_ics',
        action="store_true",
        help='Parse sheet to create the given ics')
    parser.add_argument(
        '--generate_config_from_poll',
        help='Generate the config file from poll. No other option are relevant.')
    return parser.parse_args()


# TODO refactor the matching part
# TODO do the stats per player per game
args = parse_args()

# TODO rename agenda in Availabilities
# TODO move configuration to agenda
if args.generate_config_from_poll:
    generateConfigFromPoll(args.generate_config_from_poll, args.output)
elif args.create_ics:
    configuration = Configuration(args)
    calendar = GameCalendar(args.sheet, configuration)
    calendar.write_calendars(configuration)
else:
    configuration = Configuration(args)
    agenda = Agenda(args.sheet)
    agenda.find_matches(configuration)
    agenda.display_csv(configuration)