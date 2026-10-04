# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "httpx2>=2.13.1",
#     "sense-hat ; sys_platform == 'linux'",
# ]
# ///

from datetime import date, datetime
from zoneinfo import ZoneInfo

import httpx2
from sense_hat import SenseHat  # ty: ignore[unresolved-import]  # Pi-only dep

TEAM_ID = 445  # Coachella Valley Firebirds

# Persistent httpx client for connection pooling and reuse
_http_client = httpx2.Client(timeout=30.0)


def get_todays_games() -> list[int]:
    todays_date = date.today().strftime("%Y-%m-%d")
    url = f"https://ahl.ryancheley.com/my_database/scheduled_games.json?_sort=game_id&game_date__exact={todays_date}&_labels=on"
    todays_games = httpx2.get(url).json().get("rows", [])
    return todays_games


def get_game_data(game_id: int) -> dict:
    url: str = f"https://lscluster.hockeytech.com/feed/index.php?feed=gc&tab=gamesummary&game_id={game_id}&key=ccb91f29d6744675&client_code=ahl"
    game_data = _http_client.get(url).json()
    return game_data


def get_team_name(team_id: int) -> str:
    url = "https://ahl.ryancheley.com/my_database/team.json"
    teams = httpx2.get(url).json()
    teams_rows = teams.get("rows", [])
    for team in teams_rows:
        if team[0] == team_id:
            return team[3]
    return "WTF"


def _get_game_meta_data(game_id: int, item: str):
    json_data = get_game_data(game_id)
    gc = json_data.get("GC")
    if gc is None:
        return None
    gamesummary = gc.get("Gamesummary")
    if gamesummary is None:
        return None
    meta_data = gamesummary.get("meta")
    if meta_data is None:
        return None
    meta_data_item = meta_data.get(item)
    return meta_data_item


if __name__ == "__main__":
    game_data = get_todays_games()
    sense = SenseHat()
    for game in game_data:
        game_id = game.get("game_id")
        home_team_id = game.get("home_team_id").get("value")
        home_team_name = game.get("home_team_id").get("label")
        visiting_team_id = game.get("away_team_id").get("value")
        visiting_team_name = game.get("away_team_id").get("label")
        if home_team_id == TEAM_ID or visiting_team_id == TEAM_ID:
            schedule_time = _get_game_meta_data(game_id, "schedule_time")
            timezone = _get_game_meta_data(game_id, "timezone")
            date_played = _get_game_meta_data(game_id, "date_played")
            aware_game_date = (
                datetime.strptime(f"{date_played} {schedule_time}", "%Y-%m-%d %H:%M:%S")
                .replace(tzinfo=ZoneInfo(timezone))
                .astimezone()
            )
            aware_game_date_display = aware_game_date.strftime("%I:%M %p").lstrip("0")
            message = f"The {visiting_team_name} will be playing the {home_team_name} at {aware_game_date_display}"
            sense.show_message(message, scroll_speed=0.05)
