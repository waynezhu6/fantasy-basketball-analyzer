from typing import List
import yahoo_fantasy_api as yfa
from models.matchup import Matchup
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


    def refresh(self):
        self.matchups = self.generate_matchups()


    def generate_matchups(self):
        raw_matchups = self.league.matchups()['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
        matchups = []

        for matchup_key in raw_matchups:
            if matchup_key == 'count':
                continue

            # will print list of stat_id -> value pairs
            raw_matchup = raw_matchups[matchup_key]['matchup']['0']['teams']
            # team_info = raw_matchups[matchup_key]['matchup']['0']['teams']['0']['team'][0]
            # stats = raw_matchups[matchup_key]['matchup']['0']['teams']['0']['team'][0]

            team1_key = raw_matchup['0']['team'][0][0]['team_key']
            team1_stats = raw_matchup['0']['team'][1]

            team2_key = raw_matchup['1']['team'][0][0]['team_key']
            team2_stats = raw_matchup['1']['team'][1]
            
            matchups.append(Matchup(
                self.get_team_by_team_id(team1_key),
                self.get_team_by_team_id(team2_key)
            ))

        return matchups


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
    

    def to_dict(self):
        return {
            # "teams": [team.to_dict() for team in self.teams],
            "matchups": [matchup.to_dict() for matchup in self.matchups]
        }