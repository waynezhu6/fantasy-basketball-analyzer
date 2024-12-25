from typing import List
from models.stats import Stats
from models.player import Player


class Team:

    def __init__(
        self, 
        team_key: str, 
        team_name: str,
        roster: List[Player],
        waiver_priority: int,
        roster_adds: int, 
        current_matchup_stats: Stats
    ):
        self.team_key = team_key
        self.team_name = team_name
        self.roster = roster
        self.waiver_priority = waiver_priority
        self.roster_adds = roster_adds
        self.current_matchup_stats = current_matchup_stats
        self.future_matchup_stats, self.projected_matchup_stats = \
            self._generate_matchup_stats(current_matchup_stats)
        
    
    def _generate_matchup_stats(self, current_matchup_stats: Stats):
        future_stats = Stats()
        for player in self.roster:
            future_stats = future_stats + (player.stats * player.games_remaining)
        projected_stats = current_matchup_stats + future_stats
        return future_stats, projected_stats


    def to_dict(self):
        return {
            "team_key": self.team_key,
            "team_name": self.team_name,
            "roster": [player.to_dict() for player in self.roster],
            "waiver_priority": self.waiver_priority,
            "roster_adds": self.roster_adds,
            "current_matchup_stats": self.current_matchup_stats.to_dict(),
            "future_matchup_stats": self.future_matchup_stats.to_dict(),
            "projected_matchup_stats": self.projected_matchup_stats.to_dict()
        }