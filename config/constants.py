from dataclasses import dataclass
from enum import Enum


# League Constants
LEAGUE_NAME = 'nba'
CURRENT_YEAR = 2024
LEAGUE_INDEX = 0


# Filenames
OAUTH2_JSON_FILENAME = 'oauth2.json'
PLAYER_STATS_FILENAME = 'data/player_stats.txt'


# Yahoo API Stat IDs
STAT_FG_RATIO_ID = '9004003'
STAT_FG_PCT_ID = '5'
STAT_FT_RATIO_ID = '9007006'
STAT_FT_PCT_ID = '8'
STAT_3PTM_ID = '10'
STAT_PTS_ID = '12'
STAT_REB_ID = '15'
STAT_AST_ID = '16'
STAT_STL_ID = '17'
STAT_BLK_ID = '18'
STAT_TOV_ID = '19'

# Yahoo Player Positions
class PlayerPosition(Enum):
    PG = 'PG'
    SG = 'SG'
    SF = 'SF'
    PF = 'PF'
    C = 'C'


# Player Stats
@dataclass
class PlayerStats:
    FGM: int
    FGA: int
    FTM: int
    FTA: int
    _3PTM: int
    PTS: int
    REB: int
    AST: int
    STL: int
    BLK: int
    TOV: int
    # GP: int

    def to_dict(self):
        return {
            "FGM": self.FGM,
            "FGA": self.FGA,
            "FTM": self.FTM,
            "FTA": self.FTA,
            "_3PTM": self._3PTM,
            "PTS": self.PTS,
            "REB": self.REB,
            "AST": self.AST,
            "STL": self.STL,
            "BLK": self.BLK,
            "TOV": self.TOV,
            # "GP": self.GP
        }


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
