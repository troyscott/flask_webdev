from flask import Blueprint

# Create a Blueprint
main = Blueprint('main', __name__)

from . import views, errors



