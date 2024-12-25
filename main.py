from datetime import datetime
import json
import time
import pytz
from data.schedule import refresh_schedule
from data.player_stats import refresh_stats
import schedule
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from flask import Flask, redirect, send_from_directory
from flask_cors import CORS

from config.constants import CURRENT_YEAR, LEAGUE_NAME, OAUTH2_JSON_FILENAME
from models.league import League


# Initialize flask app
app = Flask(__name__, static_folder="web/dist/assets", template_folder="web/dist")
CORS(app)


# Game setup
oauth = OAuth2(None, None, from_file=OAUTH2_JSON_FILENAME)
game = yfa.Game(oauth, LEAGUE_NAME)
leagues = []
for league_id in game.league_ids(year=CURRENT_YEAR):
    league = game.to_league(league_id)
    leagues.append(League(league))


# Serve the main React app (index.html)
@app.route("/")
def serve_react():
    return send_from_directory(app.template_folder, "index.html")

# Serve static files (CSS, JS, images, etc.)
@app.route("/assets/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


# General endpoint for all data
@app.route("/api/<league_index>")
def get_all(league_index):
    try:
        return json.dumps(leagues[int(league_index)].to_dict())
    except IndexError:
        return json.dumps({})


# Get team by team name
@app.route("/api/<league_index>/team/<team_name>")
def get_team(league_index, team_name):
    try:
        league = leagues[int(league_index)]
        for team in league.teams:
            if team.team_name == team_name:
                return json.dumps(team.to_dict())
        return json.dumps({})
    except IndexError:
        return json.dumps({})


# Catch-all route for React (handles React Router paths)
@app.route("/<path:path>")
def catch_all(path):
    return redirect("/")


# # Define the task you want to run
# def my_task():
#     oauth = OAuth2(None, None, from_file=OAUTH2_JSON_FILENAME)
#     game = yfa.Game(oauth, LEAGUE_NAME)
#     leagues = []
#     # for league_id in game.league_ids(year=CURRENT_YEAR):
#     #     league = game.to_league(league_id)
#     #     leagues.append(League(league))
#     leagues.append(League(game.to_league(game.league_ids(year=CURRENT_YEAR)[0])))
#     refresh_schedule()
#     refresh_stats()


# # Create a helper function to check the time in EST
# def is_3am_est(task_function):
#     est = pytz.timezone("US/Eastern")
#     now = datetime.now(est)
#     if now.hour == 3 and now.minute == 0:
#         task_function()


# # Schedule the function to check every minute
# schedule.every().minute.do(is_3am_est, my_task)


# # Keep the scheduler running
# while True:
#     schedule.run_pending()
#     time.sleep(1)  # Sleep to reduce CPU usage
 