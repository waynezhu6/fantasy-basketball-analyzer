from typing import List

from config.constants import PlayerPosition
from data.player_stats import get_player_stats


class Player:

    def __init__(
        self, 
        player_id: str, 
        player_name: str, 
        player_team: str,
        status: str, 
        eligible_positions: List[PlayerPosition], 
        selected_position: PlayerPosition,
        games_scheduled: int,
        games_remaining: int
    ):
        self.player_id = player_id
        self.player_name = player_name
        self.team = player_team
        self.status = status
        self.eligible_positions = eligible_positions
        self.selected_position = selected_position
        self.stats = get_player_stats(player_name)
        self.games_scheduled = games_scheduled
        self.games_remaining = games_remaining if status != "INJ" else 0
        

    def to_dict(self):
        return {
            "id": self.player_id,
            "name": self.player_name,
            "team": self.team,
            "status": self.status,
            "stats": self.stats.to_dict(),
            "games_scheduled": self.games_scheduled,
            "games_remaining": self.games_remaining,
            "eligible_positions": [pos for pos in self.eligible_positions],
            "selected_position": self.selected_position
        }
    