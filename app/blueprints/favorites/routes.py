from flask import request, jsonify 
from app.models import FavoriteTeam, db
from app.util.auth import token_required
from .schemas import favorite_schema, favorites_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import favorites_bp


# Get all favorite teams for the logged-in user
@favorites_bp.route('', methods=['GET'])
@token_required
def get_favorites():
    user_id = request.user_id  # Get user_id from token
    
    # Get all favorites for this user
    favorites = db.session.query(FavoriteTeam).filter_by(user_id=user_id).all()
    
    return jsonify({
        'favorites': favorites_schema.dump(favorites),
        'total': len(favorites)
    }), 200


# Add a new favorite team
@favorites_bp.route('', methods=['POST'])
@token_required
def add_favorite():
    user_id = request.user_id  # Get user_id from token
    
    # Load and validate the request data
    try:
        data = favorite_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if team already in favorites
    existing_favorite = db.session.query(FavoriteTeam).filter(
        FavoriteTeam.user_id == user_id,
        FavoriteTeam.team_id == data['team_id']
    ).first()
    
    if existing_favorite:
        return jsonify({'error': 'Team already in favorites'}), 400
    
    # Create new favorite with user_id from token
    data['user_id'] = user_id
    new_favorite = FavoriteTeam(**data)
    
    db.session.add(new_favorite)
    
    try:
        db.session.commit()
        return jsonify({
            "message": "Team added to favorites",
            "favorite": favorite_schema.dump(new_favorite)
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Team already in favorites'}), 400


# Remove a favorite team
@favorites_bp.route('/<int:team_id>', methods=['DELETE'])
@token_required
def remove_favorite(team_id):
    user_id = request.user_id  # Get user_id from token
    
    # Find favorite
    favorite = db.session.query(FavoriteTeam).filter(
        FavoriteTeam.user_id == user_id,
        FavoriteTeam.team_id == team_id
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Team removed from favorites"}), 200
    
    return jsonify({"error": "Favorite not found"}), 404


# Update a favorite team
@favorites_bp.route('/<int:favorite_id>', methods=['PUT'])
@token_required
def update_favorite(favorite_id):
    user_id = request.user_id  # Get user_id from token
    
    # Find the favorite
    favorite = db.session.query(FavoriteTeam).filter(
        FavoriteTeam.id == favorite_id,
        FavoriteTeam.user_id == user_id
    ).first()
    
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404
    
    # Load and validate the request data
    try:
        data = favorite_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Update favorite fields
    for key, value in data.items():
        if key != 'user_id':  # Don't allow changing user_id
            setattr(favorite, key, value)
    
    db.session.commit()
    
    return jsonify({
        "message": "Favorite updated successfully",
        "favorite": favorite_schema.dump(favorite)
    }), 200


# Get a specific favorite by ID
@favorites_bp.route('/<int:favorite_id>', methods=['GET'])
@token_required
def get_favorite(favorite_id):
    user_id = request.user_id  # Get user_id from token
    
    favorite = db.session.query(FavoriteTeam).filter(
        FavoriteTeam.id == favorite_id,
        FavoriteTeam.user_id == user_id
    ).first()
    
    if favorite:
        return favorite_schema.jsonify(favorite), 200
    return jsonify({"error": "Favorite not found"}), 404


# Delete all favorite teams for the logged-in user
@favorites_bp.route('/all', methods=['DELETE'])
@token_required
def remove_all_favorites():
    user_id = request.user_id  # Get user_id from token
    
    # Find all favorites for this user
    favorites = db.session.query(FavoriteTeam).filter_by(user_id=user_id).all()
    
    if not favorites:
        return jsonify({"error": "No favorites found"}), 404
    
    # Count how many we're deleting
    count = len(favorites)
    
    # Delete all favorites
    for favorite in favorites:
        db.session.delete(favorite)
    
    db.session.commit()
    
    return jsonify({
        "message": "All favorites removed successfully",
        "deleted_count": count
    }), 200