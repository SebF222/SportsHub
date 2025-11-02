from jose import jwt
import jose
from datetime import datetime, timedelta, timezone


SECRET_KEY = "secret signature"

def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(user_id) #converted user_id into a string so i dont get an inalid token error
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') #encoding the token 
    return token 