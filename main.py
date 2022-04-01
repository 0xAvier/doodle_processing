import argparse

from src.Configuration import Configuration
from src.Agenda import Agenda
from src.GameCalendar import GameCalendar 


def parse_args():
  parser = argparse.ArgumentParser(description='Find matching')
  parser.add_argument('-s', '--sheet', required=True)
  parser.add_argument('-c', '--config', default='config')
  parser.add_argument('-i', '--create_ics',  action="store_true", help='Parse sheet to create the given ics')
  return parser.parse_args()


# TODO refactor the matching part
# TODO do the stats per player per game
args = parse_args()
configuration = Configuration(args.config)

# TODO rename agenda in Availabilities
# TODO move configuration to agenda
if args.create_ics:
  calendar = GameCalendar(args.sheet, configuration)
  calendar.write_calendars(configuration)
else:
  agenda = Agenda(args.sheet)
  agenda.find_matches(configuration)
  agenda.display_csv(configuration)
