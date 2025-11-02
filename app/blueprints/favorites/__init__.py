from flask import Blueprint

favorites_bp = Blueprint('favorites', __name__)

from . import routes
