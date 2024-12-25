# Dataclass for a team's weekly matchup stats
from dataclasses import dataclass


@dataclass
class MatchupStats:
    # Base stats
    FGA: int
    FGM: int
    FTA: int
    FTM: int
    _3PTM: int
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

    def to_dict(self):
        return {
            "FGA": self.FGA,
            "FGM": self.FGM,
            "FTA": self.FTA,
            "FTM": self.FTM,
            "_3PTM": self._3PTM,
            "PTS": self.PTS,
            "REB": self.REB,
            "AST": self.AST,
            "STL": self.STL,
            "BLK": self.BLK,
            "TOV": self.TOV,
            "TEAM_POINTS": self.TEAM_POINTS,
            "GAMES_REMAINING": self.GAMES_REMAINING,
            "GAMES_IN_PROGRESS": self.GAMES_IN_PROGRESS,
            "GAMES_COMPLETED": self.GAMES_COMPLETED,
        }
    