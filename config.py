import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig():
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True 

    API_SPORTS_KEY = os.getenv('API_SPORTS_KEY', 'fd1f6ee47c6773eb91542203701f5dbc')

    BASKETBALL_URL = 'https://v1.basketball.api-sports.io'    
    SOCCER_URL = 'https://v3.football.api-sports.io'          
    NFL_URL = 'https://v1.american-football.api-sports.io'     
    BASEBALL_URL = 'https://v1.baseball.api-sports.io'  


    
    
class productionConfig():
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = False

    API_SPORTS_KEY = os.getenv('API_SPORTS_KEY')
    BASKETBALL_URL = 'https://v1.basketball.api-sports.io'
    SOCCER_URL = 'https://v3.football.api-sports.io'
    NFL_URL = 'https://v1.american-football.api-sports.io'
    BASEBALL_URL = 'https://v1.baseball.api-sports.io'