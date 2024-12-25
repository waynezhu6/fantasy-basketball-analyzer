from datetime import date
from typing import List
import yahoo_fantasy_api as yfa
from data.stats import to_matchup_stats_args
from models.matchup import Matchup, MatchupStats
from models.team import Team
from models.player import Player


class League:
    
    def __init__(
        self, 
        yfa_league: yfa.League,
    ):
        self._yfa_league = yfa_league
        self.refresh()


    def refresh(self):
        self.name = self._yfa_league.settings()['name']
        self.current_week = self._yfa_league.current_week()
        self.week_date_range = self._yfa_league.week_date_range(self.current_week)
        self.current_day = self._get_current_day()
        self.teams = self._generate_teams()
        self.matchups = self._generate_matchups()


    def _generate_matchups(self):
        raw_matchups = self._yfa_league.matchups()['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
        matchups = []

        for matchup_key in raw_matchups:
            if matchup_key == 'count':
                continue

            raw_matchup = raw_matchups[matchup_key]['matchup']['0']['teams']

            team1_key = raw_matchup['0']['team'][0][0]['team_key']
            team1_stats = MatchupStats(*to_matchup_stats_args(raw_matchup['0']['team'][1]))
            self.get_team_by_team_id(team1_key).set_matchup_stats(team1_stats)

            team2_key = raw_matchup['1']['team'][0][0]['team_key']
            team2_stats = MatchupStats(*to_matchup_stats_args(raw_matchup['1']['team'][1]))
            self.get_team_by_team_id(team2_key).set_matchup_stats(team2_stats)

            matchups.append(Matchup(
                self.get_team_by_team_id(team1_key),
                self.get_team_by_team_id(team2_key)
            ))

        return matchups


    def _generate_teams(self) -> List[Team]:
        yfa_league_teams = self._yfa_league.teams()
        teams = []

        for team_key in yfa_league_teams:
            team = yfa_league_teams[team_key]
            yfa_team_obj = self._yfa_league.to_team(team_key)

            new_team = Team(
                team['team_key'], 
                team['name'],
                self._generate_roster(yfa_team_obj.roster()),
                int(team['waiver_priority']),
                int(team['roster_adds']['value'])
            )
            teams.append(new_team)
        return teams


    def _generate_roster(self, raw_roster):
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
    

    def _get_current_day(self):
        current_date = date.today()
        n_days = current_date - self.week_date_range[0]
        week_total_n_days = self.week_date_range[1] - self.week_date_range[0]
        return min(n_days.days, week_total_n_days.days)
    
    
    def get_team_by_team_id(self, team_id: str) -> Team:
        for team in self.teams:
            if team.team_key == team_id:
                return team
        return None


    def to_dict(self):
        return {
            "name": self.name,
            # "teams": [team.to_dict() for team in self.teams],
            "matchups": [matchup.to_dict() for matchup in self.matchups]
        }