from typing import List
from models.player import Player


class Team:
    """Represents a team"""
    def __init__(
        self, 
        team_key: str, 
        team_name: str,
        roster: List[Player],
        waiver_priority: int,
        roster_adds: int, 
    ):
        self.team_key = team_key
        self.team_name = team_name
        self.roster = roster
        self.waiver_priority = waiver_priority
        self.roster_adds = roster_adds
        # sheets.generate_team_overview(self)

    # def initialize_roster(self):
    #     raw_roster = self.team_object.roster()
    #     for player in raw_roster:
    #         name = player['name']
    #         try:
    #             player_stats = scraper.get_stats(name)
    #             player_stats['G/W'] = self.schedule[player_stats['team']]
    #             self.roster.append(player_stats)
    #         except:
    #             print(name)

    # def generate_stats(self):
    #     stats = {
    #         "G/W": 0,
    #         "FGA/G": 0,
    #         "FGM/G": 0,
    #         "FG%": 0,
    #         "FTA/G": 0,
    #         "FTM/G": 0,
    #         "FT%": 0,
    #         "3FGM/G": 0,
    #         "PPG": 0,
    #         "RPG": 0,
    #         "APG": 0,
    #         "SPG": 0,
    #         "BPG": 0,
    #         "TPG": 0,
    #     }
    #     for player in self.roster:
    #         n_games = int(player["G/W"])
    #         for stat in player.keys():
    #             if stat in stats:
    #                 if stat != "G/W":
    #                     stats[stat] += float(player[stat]) * n_games
    #                 else:
    #                     stats["G/W"] += n_games

    #     stats["FG%"] = stats["FGM/G"] / stats["FGA/G"]
    #     stats["FT%"] = stats["FTM/G"] / stats["FTA/G"]

    #     for stat in stats.keys():
    #         if stat != "FG%" and stat != "FT%":
    #             stats[stat] = round(stats[stat], 1)
    #         else:
    #             stats[stat] = round(stats[stat], 3)
    #     self.stats = stats