from typing import List

from config.constants import PlayerPosition
from data.stats import get_player_stats, get_player_team
from data.schedule import get_team_schedule

class Player:

    def __init__(
        self, 
        player_id: str, 
        player_name: str, 
        status: str, 
        eligible_positions: List[PlayerPosition], 
        selected_position: PlayerPosition
    ):
        self.player_id = player_id
        self.player_name = player_name
        self.team = get_player_team(player_name)
        self.status = status
        self.eligible_positions = eligible_positions
        self.selected_position = selected_position
        self.stats = get_player_stats(player_name)
        self.schedule = get_team_schedule(self.team)


    def to_dict(self):
        return {
            "id": self.player_id,
            "name": self.player_name,
            "team": self.team,
            "status": self.status,
            "stats": self.stats.to_dict(),
            "eligible_positions": [pos for pos in self.eligible_positions],
            "selected_position": self.selected_position
        }
    