from datetime import date
from typing import Dict, List
import yahoo_fantasy_api as yfa
from data.schedule import get_games_played_by_team, get_games_remaining_by_team
from data.player_stats import get_player_team, to_matchup_stats_args
from models.matchup import Matchup
from models.matchup_stats import MatchupStats
from models.team import Team
from models.player import Player


class League:
    
    def __init__(self, yfa_league: yfa.League):
        self._yfa_league = yfa_league
        self.refresh()


    def refresh(self):
        self.name = self._yfa_league.settings()['name']
        self.current_week = self._yfa_league.current_week()
        self.week_date_range = self._yfa_league.week_date_range(self.current_week)
        self.current_day = self._get_current_day()
        self.teams, self.matchups = self._generate_teams_and_matchups()


    def _generate_teams_and_matchups(self):
        raw_matchups = self._yfa_league.matchups()['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
        yfa_league_teams = self._yfa_league.teams()
        matchups, teams = [], []

        for matchup_key in raw_matchups:
            if matchup_key == 'count':
                continue

            raw_matchup = raw_matchups[matchup_key]['matchup']['0']['teams']

            team1_key = raw_matchup['0']['team'][0][0]['team_key']
            team1_current_matchup_stats = MatchupStats(*to_matchup_stats_args(raw_matchup['0']['team'][1]))
            team1 = self._generate_team(
                team1_key, 
                yfa_league_teams[team1_key], 
                team1_current_matchup_stats
            )
            teams.append(team1)

            team2_key = raw_matchup['1']['team'][0][0]['team_key']
            team2_current_matchup_stats = MatchupStats(*to_matchup_stats_args(raw_matchup['1']['team'][1]))
            team2 = self._generate_team(
                team2_key, 
                yfa_league_teams[team2_key],
                team2_current_matchup_stats
            )
            teams.append(team2)

            matchups.append(Matchup(team1, team2))

        return teams, matchups


    def _generate_team(
        self, 
        team_key: str, 
        yfa_team_obj: Dict, 
        current_matchup_stats: MatchupStats
    ) -> Team:
        
        yfa_team = self._yfa_league.to_team(team_key)

        return Team(
            yfa_team_obj['team_key'], 
            yfa_team_obj['name'],
            self._generate_roster(yfa_team.roster()),
            int(yfa_team_obj['waiver_priority']),
            int(yfa_team_obj['roster_adds']['value']),
            current_matchup_stats
        )


    def _generate_roster(self, raw_roster):
        roster = []
        for player in raw_roster:
            player_team = get_player_team(player['name'])
            roster.append(Player(
                player['player_id'],
                player['name'],
                player_team,
                player['status'],
                player['eligible_positions'],
                player['selected_position'],
                get_games_played_by_team(player_team, self.current_day),
                get_games_remaining_by_team(player_team, self.current_day)
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
            "current_week": self.current_week,
            "week_date_range": [str(date) for date in self.week_date_range],
            "current_day": self.current_day,
            # "teams": [team.to_dict() for team in self.teams],
            "matchups": [matchup.to_dict() for matchup in self.matchups]
        }