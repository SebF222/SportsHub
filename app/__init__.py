#where I create the create_app function 
from flask import Flask
from .models import db
from .extensions import ma
from .blueprints.users import users_bp
from .blueprints.favorites import favorites_bp
from .blueprints.sports import sports_bp
from flask_cors import CORS

#create the application factory 
def create_app(config_name):
    
    #initialize blank app
    app = Flask(__name__)
    CORS(app)
    #configure the app
    app.config.from_object(f'config.{config_name}')

    #initialize extentions on app
    db.init_app(app)
    ma.init_app(app)

    #plug in blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(favorites_bp, url_prefix='/favorites')
    app.register_blueprint(sports_bp, url_prefix='/sports')
    return app