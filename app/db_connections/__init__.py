from flask import Blueprint

db_connections = Blueprint('db_connections', __name__)

from . import views
