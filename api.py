import requests
from datetime import datetime
from flask import Flask
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa

app = Flask(__name__)
SCHEDULE_API_URL = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"

@app.route("/")
def health_check():
    return "Healthy"

@app.route("/schedule")
def get_schedule():
    schedule = requests.get(SCHEDULE_API_URL)
    dct = {}

    for entry in schedule.json()["leagueSchedule"]["gameDates"]:
        games = entry["games"]
        lst = []
        for game in games:
            # don't include any non regular season games
            if game["seriesText"] != "":
                continue
            lst.append({
                "homeTeam": game["homeTeam"]["teamCity"] + " " + game["homeTeam"]["teamName"],
                "homeTeamId": game["homeTeam"]["teamId"],
                "awayTeam": game["awayTeam"]["teamCity"] + " " + game["awayTeam"]["teamName"],
                "awayTeamId": game["awayTeam"]["teamId"]
            })

        if lst:
            d = datetime.strptime(entry["gameDate"][:10], '%m/%d/%Y').date()
            dct[str(d)] = lst
    return dct

@app.route("/test")
def generate_teams():
    oauth = OAuth2(None, None, from_file="oauth2.json")
    game = yfa.Game(oauth, 'nba')
    league_id = game.league_ids(year=2019)
    league = game.to_league(league_id[0])  # our league of 12


if __name__ == "__main__":
    oauth = OAuth2(None, None, from_file="oauth2.json")
    if not oauth.token_is_valid():
        oauth.refresh_access_token()
    game = yfa.Game(oauth, 'nba')
    league_ids = game.league_ids(year=2023)
    league = game.to_league(league_ids[0])
    print(league.week_date_range(league.current_week()))