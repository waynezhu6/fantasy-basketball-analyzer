from dataclasses import dataclass


@dataclass
class Stats:
    # Base stats
    FGA: int = 0
    FGM: int = 0
    FTA: int = 0
    FTM: int = 0
    _3PTM: int = 0
    PTS: int = 0
    REB: int = 0
    AST: int = 0
    STL: int = 0
    BLK: int = 0
    TOV: int = 0

    # Team matchup info
    # TEAM_POINTS: int
    # GAMES_REMAINING: int
    # GAMES_IN_PROGRESS: int
    # GAMES_COMPLETED: int
    

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
            # "TEAM_POINTS": self.TEAM_POINTS,
            # "GAMES_REMAINING": self.GAMES_REMAINING,
            # "GAMES_IN_PROGRESS": self.GAMES_IN_PROGRESS,
            # "GAMES_COMPLETED": self.GAMES_COMPLETED,
        }
    

    def __add__(self, other: 'Stats') -> 'Stats':
        if isinstance(other, Stats):
            return Stats(
                round(self.FGA + other.FGA, 1),
                round(self.FGM + other.FGM, 1),
                round(self.FTA + other.FTA, 1),
                round(self.FTM + other.FTM, 1),
                round(self._3PTM + other._3PTM, 1),
                round(self.PTS + other.PTS, 1),
                round(self.REB + other.REB, 1),
                round(self.AST + other.AST, 1),
                round(self.STL + other.STL, 1),
                round(self.BLK + other.BLK, 1),
                round(self.TOV + other.TOV, 1),
                # round(self.GP + other.GP, 1)
            )
        else:
            return NotImplemented

    def __mul__(self, other: int) -> 'Stats':
        if isinstance(other, int):
            return Stats(
                round(self.FGA * other, 1),
                round(self.FGM * other, 1),
                round(self.FTA * other, 1),
                round(self.FTM * other, 1),
                round(self._3PTM * other, 1),
                round(self.PTS * other, 1),
                round(self.REB * other, 1),
                round(self.AST * other, 1),
                round(self.STL * other, 1),
                round(self.BLK * other, 1),
                round(self.TOV * other, 1),
                # round(self.GP * other, 1)
            )
        else:
            return NotImplemented
