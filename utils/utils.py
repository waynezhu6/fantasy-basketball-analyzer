import math
from typing import List
import unicodedata


def to_matchup_stats_args(raw: str) -> List[int]:
    stats = raw['team_stats']['stats']
    for raw_stat in stats:
        stat = raw_stat['stat']
        if stat['stat_id'] == '9004003':
            fgm, fga = stat['value'].split('/')
        elif stat['stat_id'] == '9007006':
            ftm, fta = stat['value'].split('/')
        elif stat['stat_id'] == '10':
            _3ptm = int(stat['value'])
        elif stat['stat_id'] == '12':
            pts = int(stat['value'])
        elif stat['stat_id'] == '15':
            reb = int(stat['value'])
        elif stat['stat_id'] == '16':
            ast = int(stat['value'])
        elif stat['stat_id'] == '17':
            stl = int(stat['value'])
        elif stat['stat_id'] == '18':
            blk = int(stat['value'])
        elif stat['stat_id'] == '19':
            tov = int(stat['value'])

    # team_points = raw['team_points']['total']
    # games_remaining = raw['team_remaining_games']['total']['remaining_games']
    # games_in_progress = raw['team_remaining_games']['total']['live_games']
    # games_completed = raw['team_remaining_games']['total']['completed_games']

    return [
        int(fgm), int(fga), int(ftm), int(fta), _3ptm, pts, reb, ast, stl, blk, tov,
        # team_points, games_remaining, games_in_progress, games_completed
    ]


def get_nba_team_abbreviation(team_name: str) -> str:
    nba_teams = {
        "Atlanta Hawks": "ATL",
        "Boston Celtics": "BOS",
        "Brooklyn Nets": "BKN",
        "Charlotte Hornets": "CHA",
        "Chicago Bulls": "CHI",
        "Cleveland Cavaliers": "CLE",
        "Dallas Mavericks": "DAL",
        "Denver Nuggets": "DEN",
        "Detroit Pistons": "DET",
        "Golden State Warriors": "GSW",
        "Houston Rockets": "HOU",
        "Indiana Pacers": "IND",
        "Los Angeles Clippers": "LAC",
        "Los Angeles Lakers": "LAL",
        "Memphis Grizzlies": "MEM",
        "Miami Heat": "MIA",
        "Milwaukee Bucks": "MIL",
        "Minnesota Timberwolves": "MIN",
        "New Orleans Pelicans": "NOP",
        "New York Knicks": "NYK",
        "Oklahoma City Thunder": "OKC",
        "Orlando Magic": "ORL",
        "Philadelphia 76ers": "PHI",
        "Phoenix Suns": "PHX",
        "Portland Trail Blazers": "POR",
        "Sacramento Kings": "SAC",
        "San Antonio Spurs": "SAS",
        "Toronto Raptors": "TOR",
        "Utah Jazz": "UTA",
        "Washington Wizards": "WAS"
    }

    return nba_teams.get(team_name)


def get_adapted_team_abbreviation(team_name: str) -> str:
    filter = {
        "GS": "GSW",
        "SA": "SAS",
        "NY": "NYK",
        "NO": "NOP",
        "PHO": "PHX",
    }
    return filter.get(team_name, team_name)


def clean_text(input_str: str) -> str:
    # Remove accents
    normalized = unicodedata.normalize('NFD', input_str)
    no_accents = ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')
    # Remove non-alphanumeric characters except apostrophes and dashes
    cleaned = ''.join(char for char in no_accents if char.isalnum() or char.isspace() or char in ("'", "-"))
    return cleaned


def get_cleaned_player_name(player_name: str) -> str:
    name = clean_text(player_name)
    interesting_names = {
        'PJ Washington Jr': 'PJ Washington',
        'Nic Claxton': 'Nicolas Claxton',
        'Alex Sarr': 'Alexandre Sarr'
    }
    return interesting_names.get(name, name)
