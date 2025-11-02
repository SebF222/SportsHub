from flask import request, jsonify 
from app.models import FavoriteTeam, db
from .schemas import favorite_schema, favorites_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import favorites_bp


# Get all favorite teams for a user
@favorites_bp.route('/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    # Get all favorites for this user
    favorites = db.session.query(FavoriteTeam).filter_by(user_id=user_id).all()
    
    return jsonify({
        'favorites': favorites_schema.dump(favorites),
        'total': len(favorites)
    }), 200


# Add a new favorite team
@favorites_bp.route('/<int:user_id>', methods=['POST'])
def add_favorite(user_id):
    # Load and validate the request data
    try:
        data = favorite_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if team already in favorites
    existing_favorite = db.session.query(FavoriteTeam).where(
        FavoriteTeam.user_id == user_id,
        FavoriteTeam.team_id == data['team_id']
    ).first()
    
    if existing_favorite:
        return jsonify({'error': 'Team already in favorites'}), 400
    
    # Create new favorite but has to extract only needed fields
    new_favorite = FavoriteTeam(
        user_id=user_id,
        team_id=data['team_id'],
        team_name=data['team_name'],
        team_logo=data['team_logo']
    )
    
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
@favorites_bp.route('/<int:user_id>/<int:team_id>', methods=['DELETE'])
def remove_favorite(user_id, team_id):
    # Find favorite
    favorite = db.session.query(FavoriteTeam).where(
        FavoriteTeam.user_id == user_id,
        FavoriteTeam.team_id == team_id
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Team removed from favorites"}), 200
    
    return jsonify({"error": "Favorite not found"}), 404


# Update a favorite team (for change of teams)
@favorites_bp.route('/<int:user_id>/<int:favorite_id>', methods=['PUT'])
def update_favorite(user_id, favorite_id):
    # Find the favorite
    favorite = db.session.query(FavoriteTeam).where(
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
        setattr(favorite, key, value)
    
    db.session.commit()
    
    return jsonify({
        "message": "Favorite updated successfully",
        "favorite": favorite_schema.dump(favorite)
    }), 200


# Get a specific favorite by ID
@favorites_bp.route('/<int:user_id>/favorite/<int:favorite_id>', methods=['GET'])
def get_favorite(user_id, favorite_id):
    favorite = db.session.query(FavoriteTeam).where(
        FavoriteTeam.id == favorite_id,
        FavoriteTeam.user_id == user_id
    ).first()
    
    if favorite:
        return favorite_schema.jsonify(favorite), 200
    return jsonify({"error": "Favorite not found"}), 404

# Delete all favorite teams for a user
@favorites_bp.route('/<int:user_id>/all', methods=['DELETE'])
def remove_all_favorites(user_id):
    # Find all favorites for this user
    favorites = db.session.query(FavoriteTeam).filter_by(user_id=user_id).all()
    
    if not favorites:
        return jsonify({"error": "No favorites found for this user"}), 404
    
    # Count how many we're deleting
    count = len(favorites)
    
    # Delete all favorites
    for favorite in favorites:
        db.session.delete(favorite)
    
    db.session.commit()
    
    return jsonify({
        "message": f"All favorites removed successfully",
        "deleted_count": count
    }), 200