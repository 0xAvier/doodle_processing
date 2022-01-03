import argparse

from src.Configuration import Configuration 
from src.Agenda import Agenda 


def parse_args():
  parser = argparse.ArgumentParser(description='Find matching')
  parser.add_argument('-s', '--sheet', required=True)
  parser.add_argument('--config', default='config')
  return parser.parse_args()


# TODO refactor the matching part
# TODO do the stats per player per game
args = parse_args()
configuration = Configuration(args.config)

agenda = Agenda(args.sheet)
agenda.find_matches(configuration)
agenda.display_csv(configuration)
