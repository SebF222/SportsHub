from app.extensions import ma
from app.models import FavoriteTeam

class FavoriteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteTeam
        include_fk = True


favorite_schema = FavoriteSchema() #handles just one user 
favorites_schema = FavoriteSchema(many=True) #handle a list of users 
favorite_schema = FavoriteSchema(exclude=['user_id'])
favorites_schema = FavoriteSchema(exclude=['user_id'])