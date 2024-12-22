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


# Dataclass for a team's weekly matchup stats
@dataclass
class MatchupStats:
    # Base stats
    FGA: int
    FGM: int
    FTA: int
    FTM: int
    PTS: int
    REB: int
    AST: int
    STL: int
    BLK: int
    TOV: int

    # Team matchup info
    TEAM_POINTS: int
    GAMES_REMAINING: int
    GAMES_IN_PROGRESS: int
    GAMES_COMPLETED: int
