from typing import List
import requests
from bs4 import BeautifulSoup

from config.constants import get_nba_team_abbreviation


def generate_schedule():
    """Gets raw html data and returns raw weekly schedule list"""
    url = "https://hashtagbasketball.com/advanced-nba-schedule-grid"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    for script in soup(['script', 'head', 'input', 'th']):
        script.extract()
    soup = soup.find('table')

    raw_schedule = {}
    for row in soup.findAll('tr'):
        cells = row.find_all(lambda tag: tag.name == "td" and tag.get("class") != ["cell-bg-1", "mw100"])
        if len(cells) == 0:
            continue
        team_name = get_nba_team_abbreviation(cells[0].text.strip())
        if team_name is None:
            continue

        games = [td.text.strip() for td in cells[2:]]
        schedule = [1 if game else 0 for game in games]
        raw_schedule[team_name] = schedule

    return raw_schedule


global schedule
schedule = generate_schedule()


def refresh_schedule():
    schedule = generate_schedule()


def get_team_schedule(team_name: str) -> List[int]:
    return schedule.get(team_name)


def get_games_played_by_team(team_name: str, current_day: int) -> int:
    return sum(get_team_schedule(team_name)[:current_day])


def get_games_remaining_by_team(team_name: str, current_day: int) -> int:
    return sum(get_team_schedule(team_name)[current_day:])

