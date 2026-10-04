# rpi-cvfirebirds

Prints the start time of any Coachella Valley Firebirds (AHL) game scheduled for today.

## Run

```bash
uv run program.py
```

`program.py` is a [PEP 723](https://peps.python.org/pep-0723/) script — `uv` reads its inline dependencies, no install step needed.

For each of today's games involving the Firebirds (team ID 445), it prints:

```
The <visitor> will be playing the <home team> at <local start time>
```

Times are converted from the game's timezone to your machine's local timezone.

## Data sources

- Schedule and team names: `ahl.ryancheley.com`
- Game metadata (start time, timezone): HockeyTech `lscluster.hockeytech.com`
