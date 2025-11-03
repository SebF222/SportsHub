import requests

from flask import current_app


class APISportsClient:
    """Client for making requests to API-Sports.io"""
    
    def __init__(self):
        self.base_url = current_app.config['API_SPORTS_URL']
        self.api_key = current_app.config['API_SPORTS_KEY']
        self.headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': self.api_key
        }
    
    def _make_request(self, endpoint, params=None):
        """
        Make API request to API-Sports.io
        Args:
            endpoint: API endpoint (e.g., 'teams', 'fixtures')
            params: Query parameters dictionary
        Returns:
            JSON response or error message
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()  # Raise error for bad status codes
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("API request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def search_teams(self, name):
        """Search teams by name"""
        return self._make_request('teams', params={'search': name})
    
    def get_team(self, team_id):
        """Get team details by ID"""
        return self._make_request('teams', params={'id': team_id})
    
    def get_team_stats(self, team_id, season, league_id):
        """
        Get team statistics
        Args:
            team_id: Team ID
            season: Season year (e.g., 2024)
            league_id: League ID
        """
        return self._make_request('teams/statistics', params={
            'team': team_id,
            'season': season,
            'league': league_id
        })
    
    def get_live_games(self):
        """Get all live games currently happening"""
        return self._make_request('fixtures', params={'live': 'all'})
    
    def get_fixtures_by_date(self, date):
        """
        Get fixtures by specific date
        Args:
            date: Date in format YYYY-MM-DD (e.g., '2024-10-29')
        """
        return self._make_request('fixtures', params={'date': date})
    
    def get_team_fixtures(self, team_id, season):
        """
        Get team's fixtures/schedule
        Args:
            team_id: Team ID
            season: Season year (e.g., 2024)
        """
        return self._make_request('fixtures', params={
            'team': team_id,
            'season': season
        })
    
    def get_player_stats(self, player_id, season):
        """
        Get player statistics
        Args:
            player_id: Player ID
            season: Season year (e.g., 2024)
        """
        return self._make_request('players', params={
            'id': player_id,
            'season': season
        })
    
    def get_leagues(self):
        """Get all available leagues"""
        return self._make_request('leagues')
    
    def get_standings(self, league_id, season):
        """
        Get league standings
        Args:
            league_id: League ID
            season: Season year (e.g., 2024)
        """
        return self._make_request('standings', params={
            'league': league_id,
            'season': season
        })