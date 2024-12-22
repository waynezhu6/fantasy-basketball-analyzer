from typing import List
from typing import List
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from config.constants import CURRENT_YEAR, LEAGUE_NAME, OAUTH2_JSON_FILENAME
from models.team import Team
from models.player import Player


class League:
    
    def __init__(
        self, 
        league: yfa.League,
    ):
        self.league = league
        self.teams = self.generate_teams()
        self.matchups = self.generate_matchups()


    def generate_matchups(self):
        raw_matchups = self.league.matchups()['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
        for matchup_key in raw_matchups:
            # will print list of stat_id -> value pairs
            raw_matchup = raw_matchups[matchup_key]['matchup']['0']['teams']
            # team_info = raw_matchups[matchup_key]['matchup']['0']['teams']['0']['team'][0]
            # stats = raw_matchups[matchup_key]['matchup']['0']['teams']['0']['team'][0]

            team1_key = raw_matchup['0']['team'][0][0]['team_key']
            team1_stats = raw_matchup['0']['team'][1]

            print(team1_stats)
            return


    def generate_teams(self) -> List[Team]:
        yfa_league_teams = self.league.teams()
        teams = []

        for team_key in yfa_league_teams:
            team = yfa_league_teams[team_key]
            yfa_team_obj = self.league.to_team(team_key)

            new_team = Team(
                team['team_key'], 
                team['name'],
                self.generate_roster(yfa_team_obj.roster()),
                team['waiver_priority'],
                team['roster_adds']['value']
            )
            teams.append(new_team)
        return teams


    def generate_roster(self,raw_roster):
        roster = []
        for player in raw_roster:
            roster.append(Player(
                player['player_id'],
                player['name'],
                player['status'],
                player['eligible_positions'],
                player['selected_position']
            ))
        return roster
    
    
    def get_team_by_team_id(self, team_id: str) -> Team:
        for team in self.teams:
            if team.team_key == team_id:
                return team
        return None