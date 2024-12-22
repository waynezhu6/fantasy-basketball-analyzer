from typing import List
from config.constants import PlayerPosition


class Player:

    def __init__(
        self, 
        player_id: str, 
        name: str, 
        status: str, 
        eligible_positions: List[PlayerPosition], 
        selected_position: PlayerPosition
    ):
        self.player_id = player_id
        self.name = name
        self.status = status
        self.eligible_positions = eligible_positions
        self.selected_position = selected_position


    def to_dict(self):
        return {
            "player_id": self.player_id,
            "name": self.name,
            "status": self.status,
            "eligible_positions": [pos for pos in self.eligible_positions],
            "selected_position": self.selected_position
        }