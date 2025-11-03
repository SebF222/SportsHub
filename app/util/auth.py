from jose import jwt
import jose
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from app.models import User, db 


SECRET_KEY = "secret signature"

def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(user_id) #converted user_id into a string so i dont get an inalid token error
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') #encoding the token 
    return token 

def decode_token(token):
    """
    Decode JWT token and return user_id
    Returns user_id as int or None if invalid (AI)
    """
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return int(data['sub'])  # return user_id as integer
    
    except jose.exceptions.ExpiredSignatureError:
        return None  # token is expired
    except jose.exceptions.JWTError:
        return None  # invalid token


def token_required(f): #wraps around a function 'f'
    @wraps(f)
    def decoration(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1] #headers: {'Authorization': "Bearer my_token"}

        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401
        
        try:

            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = int(data['sub']) #adding the user's id from the token to the request to be accesed in the wrapped function
        
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'error': 'token is expired'}), 403 # check for if its not expired 
        except jose.exceptions.JWTError:
            return jsonify({'error': 'invalid token ' }), 403  #check for if its valid 
        
        return f(*args, **kwargs)
    
    return decoration

def get_current_user():
    """
    Get the current logged-in user from JWT token
    Returns User object or None (AI)
    """
    token = None

    if 'Authorization' in request.headers:
        try:
            token = request.headers['Authorization'].split()[1]  # headers: {'Authorization': "Bearer my_token"}
        except IndexError:
            return None

    if not token:
        return None

    # decode token to get user_id
    user_id = decode_token(token)
    if not user_id:
        return None

    # find user in database
    user = db.session.get(User, user_id)
    return user

