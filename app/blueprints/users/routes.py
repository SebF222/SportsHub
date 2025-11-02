from flask import request, jsonify 
from app.models import User, db
from .schemas import user_schema, users_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import users_bp


#Register/Create User
@users_bp.route('', methods=['POST'])
def create_user():
    #Load and validate  the request data 
    try: 
        data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    data['password'] = generate_password_hash(data['password'])  #Reassigning the password to make it a hashed version of the password for security reasons

    user = db.session.query(User).where(User.email == data['email']).first() #Checking if a user exist in my database who has the same password as the one passed in 

    if user:
        return jsonify({'error': 'Email already being used.'}), 400 
    
    new_user = User(**data) #create new user
    db.session.add(new_user)
    db.session.commit()
    #create a new User in my database 

    #send a response
    return jsonify({
        "message": "successfully created user",
        "user": user_schema.dump(new_user)
    }), 201


#view profile - token auth eventually
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        return user_schema.jsonify(user), 200
    return jsonify({"error": "invalid user id"}), 400

#view all users
@users_bp.route('', methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    return users_schema.jsonify(users), 200

#update profile 

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"error": "Invalid User Id"}), 400
    
    try: 
        data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    data['password'] = generate_password_hash(data['password'])

    for key, value in data.items():
        setattr(user, key, value)

    db.session.commit()
    return jsonify({
        "message": "Succesfully updated your account",
        "user": user_schema.dump(user)
    }), 200

#Delete a user
@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.get(User, user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "successfully deleted user."}), 200
    return jsonify({"error": "invalid user id"}), 404
#signing in 