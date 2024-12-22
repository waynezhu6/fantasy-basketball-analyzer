import json
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from flask import Flask

from config.constants import CURRENT_YEAR, LEAGUE_NAME, OAUTH2_JSON_FILENAME
from models.league import League


# Game setup
oauth = OAuth2(None, None, from_file=OAUTH2_JSON_FILENAME)
game = yfa.Game(oauth, LEAGUE_NAME)
leagues = []
for league_id in game.league_ids(year=CURRENT_YEAR):
    league = game.to_league(league_id)
    leagues.append(League(league))


# General endpoint for all data
app = Flask(__name__)
@app.route("/")
def get_all():
    return json.dumps([league.to_dict() for league in leagues])
