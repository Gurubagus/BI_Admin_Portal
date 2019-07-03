from flask import Flask, session
import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import *
from flask_wtf.file import FileField, FileRequired, FileAllowed

from ..models import *

class DkronJobForm(FlaskForm):
	
	null = None
	
	#command = FileField("Python File", validators=[DataRequired()])
	#command = FileField("Python File", validators=[DataRequired()])
	schedule = StringField('Schedule', validators=[DataRequired()]) #https://dkron.io/usage/cron-spec/
	timezone = QuerySelectField(query_factory=lambda: Timezone.query.all(), get_label="name", default=lambda: Timezone.query.filter(Timezone.timezoneid == '418').one_or_none())
	owner = StringField('Owner/Job Creator', validators=[DataRequired()])
	owner_email = StringField("Owner's Email", validators=[Email()])
	executor = StringField("Executor: (default=shell)", default="shell", validators=[DataRequired()])

	#advanced options
	exec_shell= BooleanField('Executor config: Shell (default = true)', default=True)
	disable = BooleanField('Disable Job', default=False)
	tags = StringField('Tags: Target nodes tags of this job', default=null)
	retries = IntegerField('# of job retries if failed', default=0)
	
	
	submit = SubmitField('Submit')