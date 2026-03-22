# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python tool for scheduling boardgame nights. It processes Doodle poll CSV exports to match player availability with games, generates selection CSVs, and creates ICS calendar invites.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Three-step workflow:

# 1. Generate game config from a Doodle game-preference poll
./main.py --generate_config_from_poll jeux.csv -o games.ini

# 2. Generate all possible matchings CSV (pipe to file)
./main.py -c games.ini -s dates.csv > all.csv
# With separate global game config:
./main.py -c games.ini -s dates.csv -g all-games.ini > all.csv

# 3. Generate ICS calendars and stats from a selection CSV
./main.py -c games.ini -s select.csv -i
# With separate global game config:
./main.py -c games.ini -s select.csv -i -g all-games.ini
```

No test suite exists.

After editing Python files, run `autopep8 --recursive --aggressive --aggressive --in-place .` to fix formatting.

## Architecture

**Pipeline flow:** Doodle CSV poll → INI config → matching CSV → selection CSV → ICS files

- `main.py` — CLI entry point with three modes: `--generate_config_from_poll`, default (matching), `-i` (ICS generation)
- `src/Configuration.py` — Parses INI config files (`configparser`). Builds `GameCollection` and `Group` from `[games]`, `[players]`, `[players_under_reserve]`, and `[options]` sections. Supports split config: player config (`-c`) + game config (`-g`)
- `src/Agenda.py` — Parses comma-delimited availability CSVs (Doodle export). Matches players to games per date, outputs semicolon-delimited result CSV to stdout
- `src/GameCalendar.py` — Parses semicolon-delimited selection CSVs, generates per-player `.ics` files using `ics` + `arrow` libraries
- `src/ConfigFromPoll.py` — Converts a Doodle game-preference poll CSV into an INI config file
- `src/Event.py` — A date with available players and game matchings. `full_games()` filters to games with enough players and owner present
- `src/Game.py` — Game with player count ranges (e.g. "3-5" or "1,3-4") and options (`early`, `owner=Name`)
- `src/Group.py` — Collection of players + hosts with optional mandatory player
- `src/Player.py` — Player with default games and under-reserve games
- `src/GameCollection.py` — Searchable list of games

**Key concepts:**
- "Under reserve" (`Si nécessaire`/`Si besoin`) = player available but not preferred — tracked separately from confirmed ("Oui") players
- `nhosts` in options adds phantom host players to every game's player count
- `mandatory_player` must be present for a game session to count
- Game `owner` must be present for that specific game to be scheduled
- Matching CSV uses `;` delimiter; availability CSV (Doodle export) uses `,` delimiter
- In matching CSV output, "under reserve" players/dates are displayed in parentheses

## Skills

The `all-csv` skill loads a boardgame scheduling CSV and helps pick dates based on player availability, game preferences, and date ranges.
