import requests
from flask import current_app


class SoccerClient:
    
    def __init__(self):
        # getting the URL and API key from config
        self.base_url = current_app.config['SOCCER_URL']
        self.api_key = current_app.config['API_SPORTS_KEY']
        self.headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': self.api_key
        }
    
    def _make_request(self, endpoint, params=None):
        # helper method to make API calls
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Soccer API error: {str(e)}")
    
    def search_teams(self, name):
        # search for soccer teams by name
        return self._make_request('teams', params={'search': name})
    
    def get_team(self, team_id):
        # get soccer team details
        return self._make_request('teams', params={'id': team_id})
    
    def get_live_games(self):
        # get live soccer games happening now
        return self._make_request('fixtures', params={'live': 'all'})
    
    def get_games_by_date(self, date):
        # get soccer games for a specific date (YYYY-MM-DD)
        return self._make_request('fixtures', params={'date': date})