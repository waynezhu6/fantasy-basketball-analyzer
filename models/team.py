from typing import List
from models.matchup_stats import MatchupStats
from models.player import Player


class Team:

    def __init__(
        self, 
        team_key: str, 
        team_name: str,
        roster: List[Player],
        waiver_priority: int,
        roster_adds: int, 
        current_matchup_stats: MatchupStats
    ):
        self.team_key = team_key
        self.team_name = team_name
        self.roster = roster
        self.waiver_priority = waiver_priority
        self.roster_adds = roster_adds
        self.current_matchup_stats = current_matchup_stats
        self.future_matchup_stats, self.projected_matchup_stats = \
            self._generate_matchup_stats(current_matchup_stats)
        
    
    def _generate_matchup_stats(self, current_matchup_stats: MatchupStats):
        future_matchup_stats = current_matchup_stats
        projected_matchup_stats = current_matchup_stats
        return future_matchup_stats, projected_matchup_stats


    def to_dict(self):
        return {
            "team_key": self.team_key,
            "team_name": self.team_name,
            "roster": [player.to_dict() for player in self.roster],
            "waiver_priority": self.waiver_priority,
            "roster_adds": self.roster_adds,
            "current_matchup_stats": self.current_matchup_stats.to_dict(),
        }