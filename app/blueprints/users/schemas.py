from app.extensions import ma
from app.models import User
from marshmallow import validates_schema, ValidationError

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
class LoginSchema(ma.Schema): #make it so my user get to pick which they want to use out of username or email
    email = ma.String(required=False)
    username = ma.String(required=False)
    password = ma.String(required=True) 

    @validates_schema
    def validate_login_method(self, data, **kwargs):
        #make sure the email or username is getting passed in 
        if not data.get('email') and not data.get('username'):
            raise ValidationError('Either email or username must be provided')

user_schema = UserSchema() #handles just one user 
users_schema = UserSchema(many=True) #handle a list of users 
login_schema = UserSchema(exclude=['id', 'email', 'first_name', 'last_name'])
login_schema = LoginSchema()