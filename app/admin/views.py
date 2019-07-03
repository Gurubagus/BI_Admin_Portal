###################################################################################################
"""
This script holds the methods for calling on the html files for the webpages, and the delivery
of data to them.

Come here if you wish to ADD/EDIT/REMOVE the functions on any page OR update the
CHECKING OF PERMISSIONS

TABLE OF CONTENTS:

-Imports

-Check Permission Methods

-Permission Views

-Employee Views

-Organization Views

-Assign Choices Views

-Variable Views

-Source Keys Views

-Source Views

-Reporting Views

-Reporting Creation Views

-List Creation Views

-List Views

-API Views

"""
###################################################################################################


########################## Imports ################################################################

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required 
from werkzeug.utils import secure_filename
from . import admin
from forms import *
from .. import db
from ..models import *
import os
from os.path import splitext
import uuid
import requests
import json
import datetime
import sys
sys.path.insert(0, '/home/benemenadmin/dkron_jobs/json')
#import JOBPOST_dkron
from collections import OrderedDict


to_upload=""


###################################################################################################


########################## Check Permission Methods ###############################################

def check_admin():
	# prevent non-admins from accessing the page
	if not current_user.is_admin:
		abort(403)
	
def check_client_permission():
	# prevents non-authorized users from accessing through url
	
	if not current_user.role_id==2:	
		check_admin()
		
def check_BI_permission():
	# prevents non-authorized users from accessing through url
	
	if not current_user.role_id==1:		
		check_admin()


###################################################################################################



########################## Permission Views #######################################################

@admin.route('/roles')
@login_required
def list_roles():
	check_admin()
	
	"""
	List all roles
	"""
	roles = Role.query.all()
	return render_template('admin/roles/roles.html',
						   roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
	"""
	Add a role to the database
	"""
	
	check_admin()

	add_role = True

	form = RoleForm()
	if form.validate_on_submit():
		role = Role(name=form.name.data,
					description=form.description.data)

		try:
			# add role to the database
			db.session.add(role)
			db.session.commit()
			flash('You have successfully added a new role.')
		except:
			# in case role name already exists
			flash('Error: role name already exists.')

		# redirect to the roles page
		return redirect(url_for('admin.list_roles'))

	# load role template
	return render_template('admin/roles/role.html', add_role=add_role,
						   form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
	"""
	Edit a role
	"""
	
	check_admin()
	
	add_role = False

	role = Role.query.get_or_404(id)
	form = RoleForm(obj=role)
	if form.validate_on_submit():
		role.name = form.name.data
		role.description = form.description.data
		db.session.add(role)
		db.session.commit()
		flash('You have successfully edited the role.')

		# redirect to the roles page
		return redirect(url_for('admin.list_roles'))

	form.description.data = role.description
	form.name.data = role.name
	return render_template('admin/roles/role.html', add_role=add_role,
						   form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
	"""
	Delete a role from the database
	"""
	check_admin()
	
	role = Role.query.get_or_404(id)
	db.session.delete(role)
	db.session.commit()
	flash('You have successfully deleted the role.')

	# redirect to the roles page
	return redirect(url_for('admin.list_roles'))

	return render_template(title="Delete Role")

###################################################################################################


########################## Employee Views #########################################################

@admin.route('/employees')
@login_required
def list_employees():
	"""
	List all employees
	"""
	check_admin()

	employees = Employee.query.all()
	return render_template('admin/employees/employees.html',
						   employees=employees, title='Employees')

@admin.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
	"""
	Add a employee to the database
	"""
	
	check_admin()

	add_employee = True

	form = RoleForm()
	if form.validate_on_submit():
		role = Role(name=form.name.data,
					description=form.description.data)

		try:
			# add role to the database
			db.session.add(role)
			db.session.commit()
			flash('You have successfully added a new role.')
		except:
			# in case role name already exists
			flash('Error: role name already exists.')

		# redirect to the roles page
		return redirect(url_for('admin.list_roles'))

	# load role template
	return render_template('admin/roles/role.html', add_role=add_role,
						   form=form, title='Add Role')
@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
	"""
	Assign a department and a role to an employee
	"""
	check_admin()

	employee = Employee.query.get_or_404(id)


	# prevent admin from being assigned a department or role
	if employee.is_admin:
		abort(403)

	form = EmployeeAssignForm(obj=employee)
	if form.validate_on_submit():
		employee.department = form.department.data
		employee.role = form.role.data
		db.session.add(employee)
		db.session.commit()
		flash('You have successfully assigned a department and role.')

		# redirect to the roles page
		return redirect(url_for('admin.list_employees'))

	return render_template('admin/employees/employee.html',
						   employee=employee, form=form,
						   title='Assign Employee')

@admin.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required

def delete_employee(id):
	"""
	Delete an employee from the database
	"""
	check_admin()

	employee = Employee.query.get_or_404(id)
	db.session.delete(employee)
	db.session.commit()
	flash('You have successfully deleted the employee.')

	# redirect to the roles page
	return redirect(url_for('admin.list_employees'))

	return render_template('admin/employees/employee.html',
						   employee=employee, form=form,
						   title='Assign Employee')

###################################################################################################


########################## Organizations Views ####################################################

@admin.route('/organization_register', methods=['GET', 'POST'])
def organization_register():
	form = OrganizationRegistrationForm()
	if form.validate_on_submit():
		
		timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%m:%S')
		organization = Organization(org_key = uuid.uuid4(),
							short_name=form.short_name.data,
								   description=form.description.data, modified=timestamp)

			# add employee to the database
		try:
			db.session.add(organization)
			db.session.commit() 
			flash('You have successfully registered %s.' % organization.short_name)
		
		except:
			flash('%s is already registered in the database.' % organization.short_name)
			#return redirect(url_for('admin.organization_register'))
			
		return redirect(url_for('admin.list_organizations'))
	
	# load registration template
	return render_template('auth/organization_register.html', form=form, title='Organization Register')


@admin.route('/organizations')
@login_required

def list_organizations():
	"""
	List all organizations
	"""
	check_BI_permission()
#QUERY WITH ONLY ACTIVE BEING SHOWN AND ORDERING ALPHABETICALLY (FOR TOMORROW 21.2.2019)
	#organizations = Organization.query.all()
	organizations = Organization.query.filter(Organization.active==True)
	
	return render_template('admin/organizations/organizations.html',
						   organizations=organizations, title='Organizations')

@admin.route('/organizations/delete/<id>', methods=['GET', 'POST'])
@login_required

def delete_organization(id):
	"""
	Delete an organization from the database
	"""
	check_BI_permission()
	
	organization = Organization.query.get_or_404(id)
	organization.active=False
	db.session.commit()
	flash('You have successfully deleted the organization.')

	# redirect to the roles page
	return redirect(url_for('admin.list_organizations'))

	return render_template('admin/organizations/organizations.html',
						   organizations=organizations, title='Organizations')

###################################################################################################


########################## Assign Choices View ####################################################

@admin.route('/organization/assign/<id>', methods=['GET', 'POST'])
@login_required
def organization_assignment(id):
	"""
	List assign choices
	"""
	check_BI_permission()
	
	organization = Organization.query.get_or_404(id)
	
	variable_values = Variable_Values.query\
						.join(Variable)\
						.add_column(Variable_Values.org_key)\
						.add_column(Variable_Values.variable_id)\
						.add_column(Variable.variable_description)\
						.add_column(Variable_Values.var_value)\
						.filter(Variable_Values.org_key == id)\
						.filter(Variable.variable_id==Variable_Values.variable_id)
	
	source_keys = Source_Keys.query\
						.join(Data_Source)\
						.add_column(Source_Keys.org_key)\
						.add_column(Source_Keys.source_key)\
						.add_column(Source_Keys.source_id)\
						.add_column(Data_Source.short_description)\
						.filter(Source_Keys.org_key == id)
	
	reports = Report_delivery.query\
						.join(Report)\
						.join(Email_list)\
						.add_column(Report.report_name)\
						.add_column(Report.report_id)\
						.add_column(Email_list.email_description)\
						.add_column(Email_list.email_list_id)\
						.add_column(Report.report_description)\
						.add_column(Report_delivery.filters)\
						.filter(Report_delivery.org_key == id)
	
	lists = Email_list.query\
						.join(Email_recipient)\
						.add_column(Email_list.email_description)\
						.add_column(Email_list.email_list_id)\
						.add_column(Email_list.org_key)\
						.add_column(Email_recipient.email_list_id)\
						.add_column(Email_recipient.email)\
						.add_column(Email_recipient.org_key)\
						.filter(Email_list.org_key == id)
									
	return render_template('admin/organization_assign.html', 
						   organization=organization, 
						   variable_values = variable_values, 
						   source_keys = source_keys, reports=reports, lists=lists, title="Assignment")


###################################################################################################


############################# Variable Views ######################################################

@admin.route('/organizations/variables/<id>', methods=['GET', 'POST'])
@login_required
def list_org_variables(id):
	"""
	List all Variables by Organization
	"""
	check_BI_permission()
	organization = Organization.query.get_or_404(id)

	variable_values = Variable_Values.query\
						.join(Variable)\
						.add_column(Variable_Values.org_key)\
						.add_column(Variable_Values.variable_id)\
						.add_column(Variable.variable_description)\
						.add_column(Variable_Values.var_value)\
						.filter(Variable_Values.org_key == id)\
						.filter(Variable.variable_id==Variable_Values.variable_id)
	
	return render_template('admin/organization/variables/list_variables.html',
						   organization=organization, variable_values=variable_values, title='List Variables')


@admin.route('/organizations/variables/assign/<id>', methods=['GET', 'POST'])
@login_required
def assign_org_vars(id):
	"""
	Assign Variables to an organization
	"""

	check_BI_permission()
	
	organization = Organization.query.get_or_404(id)
	form = OrganizationAssignVariableForm()
	form.variable.query = Variable.query\
								.filter(Variable.variable_id.notin_([item.variable_id for item in Variable_Values.query.filter(Variable_Values.org_key==id).all()]))
	
	
	if form.validate_on_submit():
		
		timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%m:%S')
		vv = Variable_Values(org_key=organization.org_key, variable_id=form.variable.data.variable_id, 
							 var_value=form.variable_value.data, modified=timestamp)

		try:
			# add variable + value to the database
			db.session.add(vv)
			db.session.commit()
			flash('You have successfully added a new variable.')
			
		except:
			# in case variable name already exists
			flash('Error: variable already exists.')

		# redirect to list variables page
		return redirect(url_for('admin.organization_assignment', id=organization.org_key))

	return render_template('admin/organizations/organization.html', organization=organization, form=form,
						   title='Assign Variables to the Organization')

@admin.route('/organizations/variables/delete/<id>/<var_id>', methods=['GET', 'POST'])
@login_required
def delete_variable(id, var_id):
	"""
	Delete an assigned Variable from the database
	"""
	check_BI_permission()
	
	organization = Organization.query.get_or_404(id)
	variable = Variable_Values.query.filter(Variable_Values.org_key == id, Variable_Values.variable_id == var_id).delete()
	db.session.commit()
	flash('You have successfully deleted the variable.')

	# redirect to the roles page
	return redirect(url_for('admin.organization_assignment',id=organization.org_key))

	return render_template('admin/organization/organization_assign.html',
						   organization=organization, variable_values=variable_values,
						   variable_description=variable_description, title='List Variables')

#####################################################################################################


########################## Source Keys Views ########################################################

@admin.route('/organizations/sourcekeys/assign/<id>', methods=['GET', 'POST'])
@login_required
def assign_source_keys(id):
	"""
	Assign Source Keys to an organization
	"""
	check_BI_permission()

	organization = Organization.query.get_or_404(id)
	
	form = AssignSourceKeyForm()
	form.source.query = Data_Source.query\
								.filter(Data_Source.source_key.notin_([item.source_key for item in Source_Keys.query.filter(Source_Keys.org_key==id).all()]))
	
	
	if form.validate_on_submit():
		
		timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		data = Source_Keys(org_key=organization.org_key, source_key=form.source.data.source_key, source_id=form.key.data, modified=timestamp)

		try:
			db.session.add(data)
			db.session.commit()
			flash('You have successfully added a new variable.')
			
		except:
			# in case variable name already exists
			flash('Error: Source Key already exists.')

		# redirect to list variables page
		return redirect(url_for('admin.organization_assignment', id=organization.org_key))

	return render_template('admin/organizations/source_keys/source_key.html', organization=organization, form=form,
						   title='Assign Source Keys to the Organization')

@admin.route('/organizations/sourcekeys/delete/<id>/<s_id>', methods=['GET', 'POST'])
@login_required
def delete_source_keys(id, s_id):
	"""
	Delete an assigned Source Key from the database
	"""
	check_BI_permission()
	
	organization = Organization.query.get_or_404(id)
	s_id = Source_Keys.query.filter(Source_Keys.org_key == id, Source_Keys.source_id == s_id).delete()
	db.session.commit()
	flash('You have successfully deleted the Source Key.')
	
	# redirect to the roles page
	return redirect(url_for('admin.organization_assignment',id=organization.org_key))
	
	return render_template('admin/organization/organization_assign.html',
						   organization=organization, title='List Variables')
	
#####################################################################################################


########################## Source Views #############################################################	

@admin.route('/sources')
@login_required

def list_sources():
	"""
	List all sources
	"""
	check_BI_permission()

	source = Data_Source.query.all()
	return render_template('admin/organizations/source_keys/source_keys.html',
						   source=source, title='Sources')


@admin.route('/sources/register', methods=['GET', 'POST'])
def source_register():
	
	form = SourceRegistrationForm()
	if form.validate_on_submit():
		
		timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		new_source = Data_Source(source_key=uuid.uuid4(), short_description = form.source_name.data, modified=timestamp)

		try:
			db.session.add(new_source)
			db.session.commit() 
			#flash('You have successfully registered %s.' % new_source.short_description)
		
		except:
			flash('%s is already registered in the database.' % new_source.short_description)

			
		return redirect(url_for('admin.list_sources'))
	
	# load registration template
	return render_template('admin/organizations/source_keys/create_source.html', form=form, title='Source Register')


@admin.route('/organizations/sourcekeys/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_source(id):
	"""
	Delete an assigned Source Key from the database
	"""
	check_BI_permission()
	
	source = Data_Source.query.get_or_404(id)
	variable = Data_Source.query.filter(Data_Source.source_key == id).delete()
	db.session.commit()
	flash('You have successfully deleted the Source.')

	# redirect to the roles page
	return redirect(url_for('admin.list_sources'))

	return render_template('admin/variables/list_sources.html', title='List Sources')


#####################################################################################################


########################## Variable Views #############################################################	

@admin.route('/variables')
@login_required

def list_variables():
	"""
	List all variables
	"""
	check_BI_permission()

	variables = Variable.query.all()
	return render_template('admin/base/list_variables.html',
						   variables=variables, title='Variables')

@admin.route('/variables/register', methods=['GET', 'POST'])
def variable_register():
	
	form = VariableRegistrationForm()
	if form.validate_on_submit():
		
		timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		id_num= Variable.query.order_by(Variable.variable_id.desc()).first()
		num = int(id_num.variable_id) +1
		new_variable = Variable(variable_id = num, variable_name = form.variable_name.data, variable_description = form.variable_description.data,
								variable_type = form.variable_type.data, variable_default = form.variable_default.data, 
								variable_class = form.variable_class.data, variable_validator = form.variable_validator.data, modified=timestamp)

		try:
			db.session.add(new_variable)
			db.session.commit() 
			flash('You have successfully registered %s.' % new_variable.variable_name)
		
		except Exception as e:
			
			flash(e.message)

			
		return redirect(url_for('admin.list_variables'))
	
	# load registration template
	return render_template('admin/base/create_variable.html', form=form, title='Source Register')


@admin.route('/variables/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_base_variable(id):
	"""
	Delete an assigned Source Key from the database
	"""
	check_BI_permission()
	
	variable = Variable.query.get_or_404(id)
	to_del = Variable.query.filter(Variable.variable_id == id).delete()
	db.session.commit()
	flash('You have successfully deleted the Variable.')

	# redirect to the roles page
	return redirect(url_for('admin.list_variables'))

	return render_template('admin/base_variables.html', title='List Sources')





###################################################################################################


########################## Reporting Variables Views ########################################################

@admin.route('/organizations/reports/assign/<id>', methods=['GET', 'POST'])
@login_required
def assign_report(id):
	"""
	Assign Reports to an organization
	"""
	check_BI_permission()

	organization = Organization.query.get_or_404(id)
	

	form = ReportAssignmentForm()

	form.report.query = Report.query\
								.filter(Report.report_id\
								.notin_([item.report_id for item in Report_delivery\
										 .query.filter(Report_delivery.org_key==id).all()]))
	
	
	if form.validate_on_submit():
		
		data = Report_delivery(org_key=organization.org_key, 
						   report_id=form.report.data.report_id, 
						   email_list_id=form.recipient.data.email_list_id,
							filters=form.filters.data)



		try:
			# add variable + value to the database
			db.session.add(data)
			db.session.commit()
			flash('You have successfully added a new report.')
			
		except Exception as e:
			
			flash(e.message)

		# redirect to list variables page
		return redirect(url_for('admin.organization_assignment', id=organization.org_key))

	return render_template('admin/organizations/reports/report.html', organization=organization, form=form,
						   title='Assign Report to the Organization')

@admin.route('/organizations/reports/delete/<lid>/<rid>/<id>', methods=['GET', 'POST'])
@login_required
def delete_report(id, rid, lid):
	"""
	Delete an assigned Report from the database
	"""
	check_BI_permission()
	
	organization = Organization.query.get_or_404(id)
	
	try:
		report = Report_delivery.query.filter(Report_delivery.org_key == id)\
															 .filter(Report_delivery.report_id == rid)\
															 .filter(Report_delivery.email_list_id == lid)\
															 .delete()
		db.session.commit()
		flash('You have successfully deleted the report.')

	# redirect to the roles page
	
	except:
		flash('Sorry, you cannot perform this action. Please try again.')
	
	
	return redirect(url_for('admin.organization_assignment',id=organization.org_key))


#####################################################################################################


########################## Report Creation Views #############################################################	

@admin.route('/reports')
@login_required

def list_reports():
	"""
	List all reports
	"""
	check_BI_permission()

	report = Report.query.all()
	return render_template('admin/organizations/reports/list_reports.html',
						   report=report, title='Reports')


@admin.route('/reports/register', methods=['GET', 'POST'])
def report_register():
	
	form = ReportRegistrationForm()
	if form.validate_on_submit():
		timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		new_report = Report(report_name = form.report_name.data, report_description=form.report_description.data, modified=timestamp)

		try:
			db.session.add(new_report)
			db.session.commit() 
		
		except Exception as e:
			
			flash(e.message)

			
		return redirect(url_for('admin.list_reports'))
	
	# load registration template
	return render_template('admin/organizations/reports/create_report.html', form=form, title='Report Register')


@admin.route('/organizations/report/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_existing_report(id):
	"""
	Delete an assigned Source Key from the database
	"""
	check_BI_permission()
	
	variable = Report.query.filter(Report.report_id == id).delete()
	db.session.commit()
	flash('You have successfully deleted the Report.')

	# redirect to the roles page
	return redirect(url_for('admin.list_reports'))

	return render_template('admin/variables/list_reports.html', title='List Reports')




#####################################################################################################


########################## List Creation Views ####################################################	

@admin.route('/list/register/<id>', methods=['GET', 'POST'])
def contacts_register(id):
	
	organization = Organization.query.get_or_404(id)
	form = ContactRegistrationForm()
	
	if form.validate_on_submit():
		
		timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		new_c = Email_recipient(email_list_id=contactid, email = form.recipient.data, org_key = organization.id, modified=timestamp)
		new_co = Email_list(email_list_id=contactid, contact_description=form.contact_description.data, org_key = organization.id, modified=timestamp)
		try:
			db.session.add(new_c)
			db.session.add(new_co)
			db.session.commit() 
		
		except:
			flash('That contact is already registered in the database.')

			
		return redirect(url_for('admin.organization_assignment', id=organization.org_key))
	
	# load registration template
	return render_template('admin/organizations/contacts/create_contact.html', form=form, title='Contact Register')


@admin.route('/organizations/list/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_existing_contact(id):
	"""
	Delete an assigned Contact from the database
	"""
	check_BI_permission()
	
	source = Data_Source.query.get_or_404(id)
	variable = Data_Source.query.filter(Data_Source.source_key == id).delete()
	db.session.commit()
	flash('You have successfully deleted the Report.')

	# redirect to the roles page
	return redirect(url_for('admin.list_sources'))

	return render_template('admin/variables/list_sources.html', title='List Sources')

#####################################################################################################


########################## List Views ########################################################

@admin.route('/organizations/list/<id>', methods=['GET', 'POST'])
@login_required
def create_new_list(id):
	"""
	Create New Recipient List
	"""
	organization = Organization.query.get_or_404(id)
	
	form = CreateListForm()
	
	if form.validate_on_submit():
		
		timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		new_list = Email_list(email_description = form.recipient_list.data, 
								org_key = id, modified=timestamp)
		try:
			# add variable + value to the database
			db.session.add(new_list)
			db.session.commit()
			flash('You have successfully created a new list.')
			
		except:
			# in case variable name already exists
			flash('Error: Report already exists.')

		# redirect to list variables page
		return redirect(url_for('admin.organization_assignment', id=organization.org_key))
	
	return render_template('admin/organizations/contacts/create_list.html',
						   form=form, organization=organization, title='Create New List')


@admin.route('/organizations/list/assign/<id>', methods=['GET', 'POST'])
@login_required
def assign_contacts_to_list(id):
	"""
	Assign Reports to an organization
	"""
	check_BI_permission()

	organization = Organization.query.get_or_404(id)
	

	form = ContactAssignForm()
	
	if form.validate_on_submit():
		
		timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		new_contact = Email_recipient(email_list_id=form.recipient_list.data.email_list_id, 
								email = form.email.data, 
								org_key = organization.id, modified=timestamp)
	
		try:
			# add variable + value to the database
			db.session.add(contact)
			db.session.commit()
			flash('You have successfully added a new variable.')
			
		except:
			# in case variable name already exists
			flash('Error: Report already exists.')

		# redirect to list variables page
		return redirect(url_for('admin.organization_assignment', id=organization.org_key))

	return render_template('admin/organizations/contacts/create_contact.html', form=form,
						   title='Assign Contacts to the Organization')

@admin.route('/organizations/list/delete/<id>/<var_id>', methods=['GET', 'POST'])
@login_required
def delete_contact(id, var_id):
	"""
	Delete an assigned Report from the database
	"""
	check_BI_permission()
	
	organization = Organization.query.get_or_404(id)
	variable = Variable_Values.query.filter(Variable_Values.org_key == id, Variable_Values.variable_id == var_id).delete()
	db.session.commit()
	flash('You have successfully deleted the report.')

	# redirect to the roles page
	return redirect(url_for('admin.list_org_reports',id=organization.org_key))

	return render_template('admin/organizations/reports/list_contacts.html',
						   organization=organization, variable_values=variable_values,
						   variable_description=variable_description, title='Delete Report')


#####################################################################################################


########################## Company List Request Views ###############################################

@admin.route('/organizations/list/request_new/<id>/', methods=['GET','POST'])
@login_required
def request_new_list(id):
	"""
	Organization requesting new list. Will send request to BI Team for authorization and implementation
	"""
	
	organization = Organization.query.get_or_404(id)
	reports= Report_delivery.query.filter(Report_delivery.org_key==id)
	
	form = RequestNewListForm()
	
	if form.validate_on_submit():
		try:
			flash('cool man')
			return redirect(url_for('admin.organization_assignment',id=organization.org_key))
		except:
			flash('not cool dude')
	
	
	return render_template('admin/organizations/request_new_list.html',form=form,
						   organization=organization, reports=reports, title='Request New List')

#####################################################################################################


########################## Slider View ##############################################################

@admin.route('/slider.css', methods=['GET','POST'])
def slider():
	file='/home/benemenadmin/projects/BAP/app/templates/admin/slider.css'
	return redirect(url_for('admin_dashboard', filename=filename, form=form, dkron=dkron, title='Dkron'))
		
	