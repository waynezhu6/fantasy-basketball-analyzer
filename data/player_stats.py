import re
from typing import Dict, List, Optional, Tuple

import requests

from config.constants import PLAYER_STATS_FILENAME
from models.stats import Stats
from utils.utils import clean_text, get_adapted_team_abbreviation, get_cleaned_player_name


def generate_stats() -> Tuple[Dict[str, Stats], Dict[str, str]]:
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
                team = get_adapted_team_abbreviation(headers[4])
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

                player_stats[name] = Stats(*stats)
                player_teams[name] = team

    return player_stats, player_teams


global player_stats, player_teams
player_stats, player_teams = generate_stats()


def get_player_team(player_name: str) -> Optional[str]:
    player_name = get_cleaned_player_name(player_name)
    return player_teams.get(player_name, None)


def get_player_stats(player_name: str) -> Optional[Stats]:
    player_name = get_cleaned_player_name(player_name)
    return player_stats.get(player_name)


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