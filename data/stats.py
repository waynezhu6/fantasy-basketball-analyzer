import re
from typing import Dict, Optional, Tuple
import unicodedata

import requests

from config.constants import PLAYER_STATS_FILENAME, PlayerStats


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


def generate_stats() -> Tuple[Dict[str, PlayerStats], Dict[str, str]]:
    player_stats = {}
    player_teams = {}
    with open(PLAYER_STATS_FILENAME, mode="r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.strip()

            # skip if header line
            if line.startswith("R#"):
                continue

            # process player header line
            else:
                headers = line.split("\t")
                rank = int(headers[0])
                adp = headers[1]
                name = clean_text(headers[2])
                pos = headers[3]
                team = headers[4]
                gp_proj = int(headers[5])
                mpg = float(headers[6])
                
                fg_raw = re.findall(r"[\d\.]+", headers[7])
                fg = fg_raw[0]
                fgm = float(fg_raw[1])
                fga = float(fg_raw[2])

                stats = [fgm, fga]

                for i in range(9):
                    line = file.readline().strip()
                    if i == 0:
                        ft_raw = re.findall(r"[\d\.]+", line)
                        ft = ft_raw[0]
                        ftm = float(ft_raw[1])
                        fta = float(ft_raw[2])
                        stats.extend([ftm, fta])
                    elif i < 8:
                        stats.append(float(line))

                player_stats[name] = PlayerStats(*stats)
                player_teams[name] = team

    return player_stats, player_teams


global player_stats, player_teams
player_stats, player_teams = generate_stats()


def get_player_team(player_name: str) -> Optional[str]:
    player_name = get_cleaned_player_name(player_name)
    if player_name in player_teams:
        return player_teams[player_name]
    return None


def get_player_stats(player_name: str) -> Optional[PlayerStats]:
    player_name = get_cleaned_player_name(player_name)
    if player_name in player_stats:
        return player_stats[player_name]
    return None


def to_matchup_stats_args(raw: str):
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

    team_points = raw['team_points']['total']
    games_remaining = raw['team_remaining_games']['total']['remaining_games']
    games_in_progress = raw['team_remaining_games']['total']['live_games']
    games_completed = raw['team_remaining_games']['total']['completed_games']

    return [
        int(fgm), int(fga), int(ftm), int(fta), _3ptm, pts, reb, ast, stl, blk, tov,
        team_points, games_remaining, games_in_progress, games_completed
    ]


def refresh_stats():
    player_stats, player_teams = generate_stats()


# def get_stats(): 
#     # Define the URL and payload
#     url = "https://hashtagbasketball.com/fantasy-basketball-projections"

#     # Read the raw data from a file
#     with open("data/stats_request_body", "r", encoding="utf-8") as file:
#         body = file.read()

#     # Make the POST request
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
#     }
#     response = requests.post(url, data=body, headers=headers)

#     # # Print the response
#     # print(f"Status Code: {response.status_code}")
#     # print(f"Response Body: {response.text}")

#     output_file = "./response.html"
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write(response.text)



# get_stats()