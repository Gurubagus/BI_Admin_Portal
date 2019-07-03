from flask import Flask, session
import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import *
from flask_wtf.file import FileField, FileRequired, FileAllowed

from ..models import *

null = None


class DepartmentForm(FlaskForm):
	"""
	Form for admin to add or edit a department
	"""
	name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	submit = SubmitField('Submit')


class RoleForm(FlaskForm):
	"""
	Form for admin to add or edit a role
	"""
	name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
	"""
	Form for admin to assign departments and roles to employees
	"""
	department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
	role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
	submit = SubmitField('Submit')
	
class OrganizationAssignVariableForm(FlaskForm):
	"""
	Form for assigning VARIABLES to an ORGANIZATION
	"""
		
	variable = QuerySelectField("Choose Variable:", get_label="variable_description")
	variable_value = StringField('VALUE', validators=[DataRequired()])
	
	submit = SubmitField('Submit')
	
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
			
			
class ContactAssignForm(FlaskForm):
	"""
	Form to assign Contact to organizations
	"""

	company = StringField('Name', validators=[DataRequired()])
	section = StringField('Description', validators=[DataRequired()])
	email = StringField('Description', validators=[DataRequired()])
	cycle = StringField('Description', validators=[DataRequired()])
	section_field = StringField('Description', validators=[DataRequired()])
	organization_id = QuerySelectField(query_factory=lambda: Organization.query.all(),
                            get_label="name")
	submit = SubmitField('Submit')
	
	
class AssignSourceKeyForm(FlaskForm):
	"""
	Form for assigning SOURCE KEYS to an ORGANIZATION
	"""
	
	source = QuerySelectField("Sources",
                                  get_label="short_description")
	#source = QuerySelectField(query_factory=lambda: Data_Source.query.all(),
   #                               get_label="short_description")
	
	key = StringField('Key', validators=[DataRequired()])
	
	submit = SubmitField('Submit')
	
			
class SourceRegistrationForm(FlaskForm):
	"""
	Form for creating new SOURCE KEYS
	"""
	
	source_name = StringField('Source', validators=[DataRequired()])
	
	submit = SubmitField('Submit')
	
	def validate_id(self, field):
		if Data_Sources.query.filter_by(short_description=field.data).first():
			raise ValidationError('Source already in use.')

class ReportRegistrationForm(FlaskForm):
	"""
	Form for creating new REPORTS
	"""
	
	report_name = StringField('Name', validators=[DataRequired()])
	
	report_description = StringField('Description', validators=[DataRequired()])
	
	submit = SubmitField('Submit')
	
	def validate_id(self, field):
		if Data_Sources.query.filter_by(short_description=field.data).first():
			raise ValidationError('Source already in use.')


class ReportAssignmentForm(FlaskForm):
	"""
	Form for assigning REPORTS to an ORGANIZATION
	"""

	
	report = QuerySelectField(query_factory=lambda: Report.query.all(),
                                  get_label="report_description")
	
	recipient = QuerySelectField(query_factory=lambda: Email_list.query.all(),
							 						get_label="email_description")
							 					
	
	filters = StringField('Filter (Optional- Please write in SQL format)')
	
	submit = SubmitField('Submit')
	
	def validate_id(self, field):
		if Variable_Value.query.filter_by(variable_id=field.data).first():
			raise ValidationError('Variable already in use.')
			
	def validate_org_key(self, field):
		if Variable_Value.query.filter_by(org_key=field.data).first():
			raise ValidationError('Variable already in use.')

			
class ContactRegistrationForm(FlaskForm):
	"""
	Form for creating new CONTACTS
	"""
	
	email = StringField('Email', validators=[DataRequired()])
	
	contact_description = StringField('Description', validators=[DataRequired()])
	
	submit = SubmitField('Submit')
	
	def validate_id(self, field):
		if Data_Sources.query.filter_by(short_description=field.data).first():
			raise ValidationError('Source already in use.')
			
			
class ContactAssignForm(FlaskForm):
	"""
	Form for assigning CONTACTS to LISTS
	"""
	
	email = StringField('Email', validators=[DataRequired()])
	
	recipient_list = QuerySelectField(query_factory=lambda: Email_list.query.all())
	
	submit = SubmitField('Submit')
	
	def validate_id(self, field):
		if Data_Sources.query.filter_by(short_description=field.data).first():
			raise ValidationError('Source already in use.')
			
class CreateListForm(FlaskForm):
	"""
	Form for CREATING NEW LISTS
	"""
	
	recipient_list = StringField('Name/Description', validators=[DataRequired()])
	
	
	submit = SubmitField('Submit')
	
	def validate_id(self, field):
		if Data_Sources.query.filter_by(short_description=field.data).first():
			raise ValidationError('Source already in use.')
			
class RequiredIf(object):
    """
	Validates field conditionally.
    """
	
    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.iteritems():
            if name not in form._fields:
                Optional(form, field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data and not field.data:
                    Required()(form, field)
		Optional()(form, field)

class Required_If(Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)
			
		
class RequestNewListForm(FlaskForm):
	"""
	Form for SUBMITTING A REQUEST TO THE BI TEAM FOR A NEW LIST
	"""

		
	list_name = StringField('List Name', validators=[DataRequired()])
	
	which_report = QuerySelectField(query_factory=lambda: Report_delivery.query.all(),get_label="filters")
	
	yes_no_for_filter = RadioField(u'Would you like all the available information on the report delivered to this list?', choices=[
		('1','Yes, I want all the information available'),
		('0','I would like to filter the information.')], validators=[DataRequired()])
	
	filter_explanation = TextAreaField('Please explain how you would like to filter this information:', validators=[RequiredIf(yes_no_for_filter='0')])
	
	WHEN_delivery = TextAreaField('WHEN would you like this report delivered? \n (e.g. Monday @ 09:00)', validators=[DataRequired()])

	HOWOFTEN_delivery = TextAreaField('HOW OFTEN would you like this report delivered? \n (e.g. Once a week)', validators=[DataRequired()])

	submit = SubmitField('Submit')
	
			
class OptionalIfFieldEqualTo(wtf.validators.Optional):
    # a validator which makes a field optional if
    # another field has a desired value

    def __init__(self, other_field_name, value, *args, **kwargs):
        self.other_field_name = other_field_name
        self.value = value
        super(OptionalIfFieldEqualTo, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if other_field.data == self.value:
            super(OptionalIfFieldEqualTo, self).__call__(form, field)

class VariableRegistrationForm(FlaskForm):
	"""
	Form for users to create new variable entry
	"""
	
	variable_name = StringField('Company Name (Short)', validators=[DataRequired()])
	variable_description = StringField('Description', validators=[DataRequired()])
	variable_type = StringField('Type', validators=[DataRequired()])
	variable_default = StringField('Default', validators=[DataRequired()])
	variable_class = StringField('Class', validators=[DataRequired()]) 
	variable_validator = StringField('Validator', validators=[DataRequired()])
	submit = SubmitField('Submit')

	def validate_organization(self, field):
		if Variable.query.filter_by(variable_name=field.data).first():
			raise ValidationError('Organization already exists in the database.')
