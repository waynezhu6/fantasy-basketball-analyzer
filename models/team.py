from typing import List
from models.player import Player


class Team:

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
        self.matchup_stats = None
    

    def set_matchup_stats(self, matchup_stats):
        self.matchup_stats = matchup_stats


    def to_dict(self):
        return {
            "team_key": self.team_key,
            "team_name": self.team_name,
            "roster": [player.to_dict() for player in self.roster],
            "waiver_priority": self.waiver_priority,
            "roster_adds": self.roster_adds,
            "matchup_stats": self.matchup_stats.to_dict()
        }