import requests
from flask import current_app

#AI 

class NFLClient:
    
    def __init__(self):
        # getting the URL and API key from config
        self.base_url = current_app.config['NFL_URL']
        self.api_key = current_app.config['API_SPORTS_KEY']
        self.headers = {
            'x-rapidapi-host': 'v1.american-football.api-sports.io',
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
            raise Exception(f"NFL API error: {str(e)}")
    
    def search_teams(self, name):
        # search for NFL teams by name
        return self._make_request('teams', params={'search': name})
    
    def get_team(self, team_id):
        # get NFL team details
        return self._make_request('teams', params={'id': team_id})
    
    def get_live_games(self):
        # get live NFL games happening now
        return self._make_request('games', params={'live': 'all'})
    
    def get_games_by_date(self, date):
        # get NFL games for a specific date (YYYY-MM-DD)
        return self._make_request('games', params={'date': date})