---
name: all.csv
description: Load a boardgame scheduling CSV and help pick dates based on user constraints (player availability, game preferences, date ranges).
disable-model-invocation: false
allowed-tools: Read
user-invocable: true
args: file_path
---

# Boardgame Scheduling CSV Helper

## Purpose

Load and interpret a boardgame scheduling CSV file so you can help the user pick the best dates to play specific games based on their constraints.

## How to use

1. Read the file at the path provided as argument (default: `all.csv` in the current working directory).
2. Parse it according to the format described below.
3. Ask the user what they need help with (e.g. "When can we play Arcs with at least 4 people?" or "What's the best date for Nemesis?").
4. Answer by filtering and ranking dates from the parsed data.

## CSV Format

The file is a semicolon-delimited CSV with this structure:

### Row 1 — Header
- First cell is empty.
- Remaining cells are game names followed by match counts, e.g. `Arcs 38 matches`.
- Games are sorted left-to-right from fewest matches (hardest to schedule) to most matches (easiest).

### Row 2 — Blank separator

### Remaining rows — Date entries or blank separators
- **Blank rows** separate weeks (inserted before each Monday).
- **Date rows**:
  - First cell: the date in `YYYY-MM-DD` format.
  - Following cells correspond to the games in the header (same column order).
  - An empty cell means the game cannot be played on that date (not enough players or mandatory player absent).
  - A non-empty cell contains a match description with this format:

```
<player_count>: <confirmed_players>, (<reserve_players>)
```

Where:
- `<player_count>` is either `Np` (exactly N players, fits the game's range) or `N/Mp` (M players available but the game supports up to N, meaning some would sit out or there's a slight overflow).
- `<confirmed_players>` are players who said "Oui" (definitely available).
- `<reserve_players>` (in parentheses) are players who said "Si besoin" (available if needed).

### Example cell values
- `4p: Arnaud, Carl, Guillaume, Xavier` — exactly 4 confirmed players, fits the game.
- `3/5p: Arnaud, D2, Guillaume, (Nico VH, Quentin)` — 3 confirmed + 2 reserve = 5 total; game supports 3 but not 5, so 3/5p indicates a range issue.
- Empty cell — game can't be played that date.

## Key concepts

- **Mandatory player**: Some configurations require a specific player (often "Guillaume") to be present. Dates where this player is absent have entirely empty rows.
- **Confirmed vs reserve**: Confirmed players ("Oui") are reliable. Reserve players ("Si besoin") might come but are uncertain.
- **Player count notation**: `N/Mp` means M people are available but the game's ideal range caps at N. The first number is the game's closest valid player count, the second is the actual available count.

## How to help the user

When the user asks to pick dates, consider:

1. **Game preference**: Filter to columns for the requested game(s).
2. **Date range**: Filter to the requested time window.
3. **Minimum confirmed players**: Prefer dates with more confirmed (non-reserve) players.
4. **Specific players**: Filter to dates where named players appear (in either confirmed or reserve).
5. **Avoid conflicts**: If multiple games are desired, find dates that work for several.
6. **Rank by quality**: Prefer dates with exact player count matches (`4p`) over overflow (`3/5p`), and more confirmed players over more reserve players.

Always present results as a clear list of recommended dates with the relevant details.
