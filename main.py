from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa

from config.constants import CURRENT_YEAR, LEAGUE_NAME, OAUTH2_JSON_FILENAME
from models.league import League


if __name__ == "__main__":
    oauth = OAuth2(None, None, from_file=OAUTH2_JSON_FILENAME)
    game = yfa.Game(oauth, LEAGUE_NAME)
    league_ids = game.league_ids(year=CURRENT_YEAR)
    league = game.to_league(league_ids[0])
    League(league)
