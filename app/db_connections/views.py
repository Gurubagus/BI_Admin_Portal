########################## Imports ################################################################

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required 
from werkzeug.utils import secure_filename
from . import db_connections
from forms import *
from .. import db
from ..models import *
import os
from os.path import splitext
import uuid
import requests
import json
import datetime
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



########################## DBCon Views #######################################################

@db_connections.route('/dbconnections')
@login_required
def list_db_connections():
	check_admin()
	
	"""
	List all database connections
	"""
	dbcon = Db_connection.query.all()
	return render_template('admin/db_connections/db_connections.html',
						   dbcon=dbcon, title='DB Connections')

@db_connections.route('/dbconnections/add', methods=['GET', 'POST'])
@login_required
def add_db_connections():
	"""
	Add a role to the database
	"""
	
	check_admin()

	add_role = True

	form = DBConnectionForm()
	if form.validate_on_submit():
		dbcon = Db_connection(name=form.name.data,
							  server=form.server.data,
							  port=form.port.data,
							  database=form.database.data,
							  login=form.login.data,
							  password=form.password.data,
							  additionalparams=form.additionalparams.data,
							  system_type=form.system_type.data,
							  active=form.active.data)

		try:
			# add role to the database
			db.session.add(dbcon)
			db.session.commit()
			flash('You have successfully added a new database connection.')
		except:
			# in case role name already exists
			flash('Error: role name already exists.')

		# redirect to the roles page
		return redirect(url_for('db_connections.list_db_connections'))

	# load role template
	return render_template('admin/db_connections/create_db_connection.html', form=form, title='Add Connection')


@db_connections.route('/dbconnections/edit/<name>', methods=['GET', 'POST'])
@login_required
def edit_db_connections(name):
	"""
	Edit a db connection
	"""
	
	check_admin()
	
	add_role = False

	role = Db_connection.query.get_or_404(name)
	form = RoleForm(obj=role)
	if form.validate_on_submit():
		role.name = form.name.data
		role.description = form.description.data
		
		db.session.commit()
		flash('You have successfully edited the role.')

		# redirect to the roles page
		return redirect(url_for('admin.list_roles'))

	form.description.data = role.description
	form.name.data = role.name
	return render_template('admin/roles/role.html', add_role=add_role,
						   form=form, title="Edit Role")

@db_connections.route('/dbconnections/activate/<name>', methods=['GET', 'POST'])
@login_required
def activate_db_connections(name):
	
	check_admin()
	print("is it reaching the method?")
	dbcon = Db_connection.query.get_or_404(name)
	dbcon.active=True
	db.session.commit()
	flash('You have successfully activated the database connection.')

	# redirect to the db connection page
	return redirect(url_for('db_connections.list_db_connections'))

@db_connections.route('/dbconnections/deactivate/<name>', methods=['GET', 'POST'])
@login_required
def deactivate_db_connections(name):
	
	check_admin()
	
	dbcon = Db_connection.query.get_or_404(name)
	dbcon.active=False
	db.session.commit()
	flash('You have successfully deactivated the database connection.')

	# redirect to the db connection page
	return redirect(url_for('db_connections.list_db_connections'))
	
	
@db_connections.route('/dbconnections/delete/<name>', methods=['GET', 'POST'])
@login_required
def delete_db_connections(name):
	"""
	Delete a role from the database
	"""
	check_admin()
	
	dbcon = Db_connection.query.get_or_404(name)
	db.session.delete(dbcon)
	db.session.commit()
	flash('You have successfully deleted the database connection.')

	# redirect to the roles page
	return redirect(url_for('db_connections.list_db_connections'))
