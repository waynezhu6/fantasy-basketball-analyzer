from enum import Enum

# League Constants
OAUTH2_JSON_FILENAME = "oauth2.json"
LEAGUE_NAME = "nba"
CURRENT_YEAR = 2024
LEAGUE_INDEX = 0

# Yahoo Player Position Enum
class PlayerPosition(Enum):
    PG = "PG"
    SG = "SG"
    SF = "SF"
    PF = "PF"
    C = "C"

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