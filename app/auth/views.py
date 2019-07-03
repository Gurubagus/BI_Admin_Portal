from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee, Department, Role, Organization, Source_Keys, Variable, Variable_Values, Report
import uuid

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		
		timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		employee = Employee(email=form.email.data,
							username=form.username.data,
							first_name=form.first_name.data,
							last_name=form.last_name.data,
							password=form.password.data, modified=timestamp)

		# add employee to the database
		db.session.add(employee)
		db.session.commit() 
		flash('You have successfully registered %s. Please log in as employee to verify functionality.' % employee.username)

		# redirect to the login page
		return redirect(url_for('auth.login'))

	# load registration template
	return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():

		# check whether employee exists in the database and whether
		# the password entered matches the password in the database
		employee = Employee.query.filter_by(email=form.email.data).first()
		if employee is not None and employee.verify_password(form.password.data):
			# log employee in
			login_user(employee)
			
			#session[employee]= employee.id
			#session['urls'] = []

			# redirect to the appropriate dashboard page
			if employee.is_admin:
				return redirect(url_for('home.admin_dashboard'))
			
			elif employee.role_id==1:
				return redirect(url_for('home.biteam_dashboard'))
			
			elif employee.role_id==2:
				return redirect(url_for('home.client_dashboard'))
			else:
				
				return redirect(url_for('home.dashboard'))

		# when login details are incorrect
		else:
			flash('Invalid email or password.')

	# load login template
	return render_template('auth/login.html', form=form, title='Login')

"""
@auth.after_request
def store_visited_urls():
	session['urls'].append(request.url)
	if len(session['urls']) > 5:
	   session['urls'].pop(0)
	session.modified = True
"""

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have successfully been logged out.')

	# redirect to the login page
	return redirect(url_for('auth.login'))