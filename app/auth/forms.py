from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee


class RegistrationForm(FlaskForm):
	"""
	Form for users to create new account
	"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	username = StringField('Username', validators=[DataRequired()])
	first_name = StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(),
													 EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password')
	submit = SubmitField('Register')

	def validate_email(self, field):
		if Employee.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already in use.')

	def validate_username(self, field):
		if Employee.query.filter_by(username=field.data).first():
			raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
	"""
	Form for users to login
	"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')
	

class OrganizationRegistrationForm(FlaskForm):
	"""
	Form for users to create organization entry
	"""
	
	short_name = StringField('Company Name (Short)', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	submit = SubmitField('Submit')

	def validate_organization(self, field):
		if Organization.query.filter_by(company_name=field.data).first():
			raise ValidationError('Organization already exists in the database.')

	def validate_id(self, field):
		if Organization.query.filter_by(organization_id=field.data).first():
			raise ValidationError('Organization ID is already in use.')
			
class VariableRegistrationForm(FlaskForm):
	"""
	Form for users to create qlik load variable entry
	"""
	variable_id = StringField('Variable ID', validators=[DataRequired()])
	variable_name = StringField('Variable', validators=[DataRequired()])
	value = StringField('Value', validators=[DataRequired()])

	submit = SubmitField('Submit')

	def validate_variable(self, field):
		if Variable.query.filter_by(variable_name=field.data).first():
			raise ValidationError('Variable already exists in the database.')
			

class ReportRegistrationForm(FlaskForm):
	"""
	Form for users to create qlik load variable entry
	"""
	report_id = StringField('Report ID', validators=[DataRequired()])
	report_name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])

	submit = SubmitField('Submit')

	def validate_report(self, field):
		if Report.query.filter_by(report_name=field.data).first():
			raise ValidationError('Report already exists in the database.')
			
class EmailRegistrationForm(FlaskForm):
	"""
	Form for users to create qlik load variable entry
	"""
	email_id = StringField('Report ID', validators=[DataRequired()])
	email = StringField('Name', validators=[DataRequired()])

	submit = SubmitField('Submit')

	def validate_report(self, field):
		if Report.query.filter_by(report_name=field.data).first():
			raise ValidationError('Report already exists in the database.')
			

