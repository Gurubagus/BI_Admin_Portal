from flask import Flask, session
import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import *
from flask_wtf.file import FileField, FileRequired, FileAllowed

from ..models import *

class APIGetInfo(FlaskForm):
	
	company1 = StringField('Company:', validators=[DataRequired()])
	
	submit1 = SubmitField('Submit')
	
class APIXRM(FlaskForm):
	
	company2 = StringField('Company:(XRM)', validators=[DataRequired()])
		
	submit2 = SubmitField('Submit')	

class APIFileCopier(FlaskForm):
	
	app = QuerySelectField(query_factory=lambda: APP.query.all(), get_label="name")
	company3 = StringField('Company (short name)', validators=[DataRequired()])
		
	submit3 = SubmitField('Submit')	