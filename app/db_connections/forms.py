from flask import Flask, session
import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import *

from ..models import *

null = None

class DBConnectionForm(FlaskForm):
	"""
	Form to assign Contact to organizations
	"""

	name = StringField('Name', validators=[DataRequired()])
	server = StringField('Server', validators=[DataRequired()])
	port = IntegerField('Port', validators=[DataRequired()])
	database = StringField('Database', validators=[DataRequired()])
	login = StringField('login', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])
	additionalparams = StringField('Additional Parameters')
	system_type = StringField('System Type', validators=[DataRequired()])
	active = BooleanField('Active', default=True)
	
	submit = SubmitField('Submit')
	
