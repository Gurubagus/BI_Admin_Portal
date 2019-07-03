from flask import Flask, session
import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import *
from flask_wtf.file import FileField, FileRequired, FileAllowed

from ..models import *

class ChooseCompany(FlaskForm):
	
	formal = StringField('Username (e.g. Benemen Training)', validators=[DataRequired()])
	company = StringField('Company Short Name (to search db)', validators=[DataRequired()])
	
	submit = SubmitField('Submit')
	
