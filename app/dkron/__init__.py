from flask import Blueprint

dkron = Blueprint('dkron', __name__)

from . import views
