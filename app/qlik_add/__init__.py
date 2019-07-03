from flask import Blueprint

qlik_add = Blueprint('qlik_add', __name__)

from . import views
