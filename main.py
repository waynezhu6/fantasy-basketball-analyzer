from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import scraper
import sheets


class FantasyTeam:
    """Represents a team"""
    def __init__(self, name, team_object, schedule):
        self.name = name
        self.team_object = team_object
        self.roster = []
        self.schedule = schedule
        self.stats = {}
        self.initialize_roster()
        self.generate_stats()
        sheets.generate_team_overview(self)

    def initialize_roster(self):
        raw_roster = self.team_object.roster()
        for player in raw_roster:
            name = player['name']
            try:
                player_stats = scraper.get_stats(name)
                player_stats['G/W'] = self.schedule[player_stats['team']]
                self.roster.append(player_stats)
            except:
                print(name)

    def generate_stats(self):
        stats = {
            "G/W": 0,
            "FGA/G": 0,
            "FGM/G": 0,
            "FG%": 0,
            "FTA/G": 0,
            "FTM/G": 0,
            "FT%": 0,
            "3FGM/G": 0,
            "PPG": 0,
            "RPG": 0,
            "APG": 0,
            "SPG": 0,
            "BPG": 0,
            "TPG": 0,
        }
        for player in self.roster:
            n_games = int(player["G/W"])
            for stat in player.keys():
                if stat in stats:
                    if stat != "G/W":
                        stats[stat] += float(player[stat]) * n_games
                    else:
                        stats["G/W"] += n_games

        stats["FG%"] = stats["FGM/G"] / stats["FGA/G"]
        stats["FT%"] = stats["FTM/G"] / stats["FTA/G"]

        for stat in stats.keys():
            if stat != "FG%" and stat != "FT%":
                stats[stat] = round(stats[stat], 1)
            else:
                stats[stat] = round(stats[stat], 3)
        self.stats = stats


def generate_teams(teamnames=None):
    oauth = OAuth2(None, None, from_file="oauth2.json")
    game = yfa.Game(oauth, 'nba')
    league_id = game.league_ids(year=2019)
    league = game.to_league(league_id[0])  # our league of 12

    teams_ids = league.teams()  # array of team ids in this league
    teams = []

    schedule = scraper.get_schedule()

    for team_id in teams_ids:
        team_obj = league.to_team(team_id['team_key'])
        if teamnames:
            if team_id['name'] in teamnames:
                new_team = FantasyTeam(team_id['name'], team_obj, schedule)
                teams.append(new_team)
                print(new_team.stats, new_team.name)
        else:
            new_team = FantasyTeam(team_id['name'], team_obj, schedule)
            teams.append(new_team)
            print(new_team.stats, new_team.name)
    return teams


if __name__ == "__main__":
    league_teams = generate_teams()
    sheets.generate_overview(league_teams)
