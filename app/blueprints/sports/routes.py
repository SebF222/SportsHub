from flask import request, jsonify
from app.blueprints.sports.basketball_client import BasketballClient
from app.blueprints.sports.soccer_client import SoccerClient
from app.blueprints.sports.nfl_client import NFLClient
from app.blueprints.sports.baseball_client import BaseballClient
from . import sports_bp



# search basketball teams
@sports_bp.route('/basketball/teams/search', methods=['GET'])
def search_basketball_teams():
    name = request.args.get('name')
    
    if not name:
        return jsonify({'error': 'Team name is required'}), 400
    
    try:
        client = BasketballClient()
        result = client.search_teams(name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get basketball team details
@sports_bp.route('/basketball/teams/<int:team_id>', methods=['GET'])
def get_basketball_team(team_id):
    try:
        client = BasketballClient()
        result = client.get_team(team_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get live basketball games
@sports_bp.route('/basketball/games/live', methods=['GET'])
def get_live_basketball_games():
    try:
        client = BasketballClient()
        result = client.get_live_games()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get basketball games by date
@sports_bp.route('/basketball/games/date', methods=['GET'])
def get_basketball_games_by_date():
    date = request.args.get('date')
    
    if not date:
        return jsonify({'error': 'Date is required (YYYY-MM-DD)'}), 400
    
    try:
        client = BasketballClient()
        result = client.get_games_by_date(date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get NFL games by date
@sports_bp.route('/nfl/games/date', methods=['GET'])
def get_nfl_games_by_date():
    date = request.args.get('date')
    
    if not date:
        return jsonify({'error': 'Date is required (YYYY-MM-DD)'}), 400
    
    try:
        client = NFLClient()
        result = client.get_games_by_date(date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# search baseball teams
@sports_bp.route('/baseball/teams/search', methods=['GET'])
def search_baseball_teams():
    name = request.args.get('name')
    
    if not name:
        return jsonify({'error': 'Team name is required'}), 400
    
    try:
        client = BaseballClient()
        result = client.search_teams(name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get baseball team details
@sports_bp.route('/baseball/teams/<int:team_id>', methods=['GET'])
def get_baseball_team(team_id):
    try:
        client = BaseballClient()
        result = client.get_team(team_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get live baseball games
@sports_bp.route('/baseball/games/live', methods=['GET'])
def get_live_baseball_games():
    try:
        client = BaseballClient()
        result = client.get_live_games()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get baseball games by date
@sports_bp.route('/baseball/games/date', methods=['GET'])
def get_baseball_games_by_date():
    date = request.args.get('date')
    
    if not date:
        return jsonify({'error': 'Date is required (YYYY-MM-DD)'}), 400
    
    try:
        client = BaseballClient()
        result = client.get_games_by_date(date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# search NFL teams
@sports_bp.route('/nfl/teams/search', methods=['GET'])
def search_nfl_teams():
    name = request.args.get('name')
    
    if not name:
        return jsonify({'error': 'Team name is required'}), 400
    
    try:
        client = NFLClient()
        result = client.search_teams(name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get NFL team details
@sports_bp.route('/nfl/teams/<int:team_id>', methods=['GET'])
def get_nfl_team(team_id):
    try:
        client = NFLClient()
        result = client.get_team(team_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get live NFL games
@sports_bp.route('/nfl/games/live', methods=['GET'])
def get_live_nfl_games():
    try:
        client = NFLClient()
        result = client.get_live_games()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# search soccer teams
@sports_bp.route('/soccer/teams/search', methods=['GET'])
def search_soccer_teams():
    name = request.args.get('name')
    
    if not name:
        return jsonify({'error': 'Team name is required'}), 400
    
    try:
        client = SoccerClient()
        result = client.search_teams(name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get soccer team details
@sports_bp.route('/soccer/teams/<int:team_id>', methods=['GET'])
def get_soccer_team(team_id):
    try:
        client = SoccerClient()
        result = client.get_team(team_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get live soccer games
@sports_bp.route('/soccer/games/live', methods=['GET'])
def get_live_soccer_games():
    try:
        client = SoccerClient()
        result = client.get_live_games()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# get soccer games by date
@sports_bp.route('/soccer/games/date', methods=['GET'])
def get_soccer_games_by_date():
    date = request.args.get('date')
    
    if not date:
        return jsonify({'error': 'Date is required (YYYY-MM-DD)'}), 400
    
    try:
        client = SoccerClient()
        result = client.get_games_by_date(date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


