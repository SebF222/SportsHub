from flask import Blueprint

sports_bp = Blueprint('sports', __name__)

from . import routes