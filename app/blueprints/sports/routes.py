from flask import request, jsonify
from app.blueprints.sports.api_client import APISportsClient
from . import sports_bp


# Search for teams by name
@sports_bp.route('/teams/search', methods=['GET'])
def search_teams():
    """
    Search for teams by name
    Query params: ?name=<team_name>
    Example: /sports/teams/search?name=Lakers
    """
    name = request.args.get('name')
    
    if not name:
        return jsonify({'error': 'Team name is required'}), 400
    
    try:
        client = APISportsClient()
        result = client.search_teams(name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch teams', 'message': str(e)}), 500


# Get team details by ID
@sports_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """
    Get team details
    Example: /sports/teams/145
    """
    try:
        client = APISportsClient()
        result = client.get_team(team_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch team', 'message': str(e)}), 500


# Get team statistics
@sports_bp.route('/teams/<int:team_id>/stats', methods=['GET'])
def get_team_stats(team_id):
    """
    Get team statistics
    Query params: ?season=<year>&league=<league_id>
    Example: /sports/teams/145/stats?season=2024&league=39
    """
    season = request.args.get('season')
    league_id = request.args.get('league')
    
    if not season or not league_id:
        return jsonify({'error': 'Season and league are required'}), 400
    
    try:
        client = APISportsClient()
        result = client.get_team_stats(team_id, season, league_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch team stats', 'message': str(e)}), 500


# Get team schedule/fixtures
@sports_bp.route('/teams/<int:team_id>/schedule', methods=['GET'])
def get_team_schedule(team_id):
    """
    Get team's schedule/fixtures
    Query params: ?season=<year>
    Example: /sports/teams/145/schedule?season=2024
    """
    season = request.args.get('season')
    
    if not season:
        return jsonify({'error': 'Season is required'}), 400
    
    try:
        client = APISportsClient()
        result = client.get_team_fixtures(team_id, season)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch team schedule', 'message': str(e)}), 500


# Get live games
@sports_bp.route('/games/live', methods=['GET'])
def get_live_games():
    """
    Get all live games currently happening
    Example: /sports/games/live
    """
    try:
        client = APISportsClient()
        result = client.get_live_games()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch live games', 'message': str(e)}), 500


# Get games by date
@sports_bp.route('/games/date', methods=['GET'])
def get_games_by_date():
    """
    Get games by specific date
    Query params: ?date=<YYYY-MM-DD>
    Example: /sports/games/date?date=2024-10-29
    """
    date = request.args.get('date')
    
    if not date:
        return jsonify({'error': 'Date is required (format: YYYY-MM-DD)'}), 400
    
    try:
        client = APISportsClient()
        result = client.get_fixtures_by_date(date)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch games', 'message': str(e)}), 500


# Get player statistics
@sports_bp.route('/players/<int:player_id>', methods=['GET'])
def get_player_stats(player_id):
    """
    Get player statistics
    Query params: ?season=<year>
    Example: /sports/players/276/stats?season=2024
    """
    season = request.args.get('season')
    
    if not season:
        return jsonify({'error': 'Season is required'}), 400
    
    try:
        client = APISportsClient()
        result = client.get_player_stats(player_id, season)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch player stats', 'message': str(e)}), 500


# Get all leagues
@sports_bp.route('/leagues', methods=['GET'])
def get_leagues():
    """
    Get all available leagues
    Example: /sports/leagues
    """
    try:
        client = APISportsClient()
        result = client.get_leagues()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch leagues', 'message': str(e)}), 500


# Get league standings
@sports_bp.route('/leagues/<int:league_id>/standings', methods=['GET'])
def get_standings(league_id):
    """
    Get league standings
    Query params: ?season=<year>
    Example: /sports/leagues/39/standings?season=2024
    """
    season = request.args.get('season')
    
    if not season:
        return jsonify({'error': 'Season is required'}), 400
    
    try:
        client = APISportsClient()
        result = client.get_standings(league_id, season)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch standings', 'message': str(e)}), 500