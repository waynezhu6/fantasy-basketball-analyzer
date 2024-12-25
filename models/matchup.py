from dataclasses import dataclass
from models.team import Team


# Matchup dataclass
@dataclass
class Matchup:
    team1: Team
    team2: Team

    def to_dict(self):
        return {
            "0": self.team1.to_dict(),
            "1": self.team2.to_dict(),
        }
