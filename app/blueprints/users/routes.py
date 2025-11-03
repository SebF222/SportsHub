from flask import request, jsonify 
from app.models import User, db
from app.util.auth import encode_token, token_required
from .schemas import user_schema, users_schema, login_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import users_bp



#signing in 
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = login_schema.load(request.json) #unpacking email and password
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    user = None 
    
    # if statement for whether the user desides to log in with either their email or username
    if data.get('email'):
        user = db.session.query(User).filter(User.email == data['email']).first()#checking if a user belongs to this email

    elif data.get('username'):
        user = db.session.query(User).filter(User.username == data['username']).first()

    if user and check_password_hash(user.password, data['password']): #if we found user with that email, then check that users email against the email that was passed in 
        token = encode_token(user.id)
        return jsonify({
            "message": "Succesfully logged in",
            "token": token,
            "user": user_schema.dump(user)
        }), 200 
    
    return jsonify({'error': 'invalid  username/email or password'}), 404

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
@users_bp.route('', methods=['GET'])
@token_required
def get_user():
    user_id = request.user_id
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

@users_bp.route('', methods=['PUT'])
@token_required
def update_user():
    user_id = request.user_id #grabbing the user id from the request 
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
@users_bp.route('', methods=['DELETE'])
@token_required
def delete_user():
    user_id = request.user_id
    user = db.session.get(User, user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "successfully deleted user."}), 200
    return jsonify({"error": "invalid user id"}), 404
