from flask import abort, render_template
from flask_login import current_user, login_required
from . import home
import sys
sys.path.append("/home/benemenadmin/PyResources")
from gpconnect import GP_Connect, Timestamp_Update, Log_Table, Qlik_Connect
import uuid


@home.route('/')
@login_required
def homepage():
	"""
	Render the homepage template on the / route
	"""
	
	data = []
	
	if 'urls' in session:
		data = session['urls']
		return render_template(data[1], data=data)
	else:
		if current_user.role_id==1: #BITeam role_id = 1
			return render_template('home/biteam_dashboard.html', title="Welcome")

		elif current_user.role_id==2:#Client role_id = 2
			return render_template('home/client_dashboard.html', title="Welcome")

		elif current_user.is_admin:
			return render_template('home/admin_dashboard.html', title="Welcome")

		else:
			abort(403)
		

@home.route('/dashboard')
@login_required
def dashboard():
	"""
	Render the dashboard template on the /dashboard route
	"""
	
	if current_user.role_id==1: #BITeam role_id = 5
		return render_template('home/biteam_dashboard.html', title="Welcome")
	
	elif current_user.role_id==2:#Client role_id = 2
		return render_template('home/client_dashboard.html', title="Welcome")
	
	elif current_user.is_admin:
		return render_template('home/admin_dashboard.html', title="Welcome")
	
	else:
		abort(403)

@home.route('/admin/uuidgenerator.js')
@login_required
def uuid_generator():
	# prevent non-admins from accessing the page
	if not current_user.is_admin:
		abort(403)

	return render_template('home/uuidgenerator.js', title="Admin Homepage")

@home.route('/admin/passwordgenerator.js')
@login_required
def upasswordgenerator():
	# prevent non-admins from accessing the page
	if not current_user.is_admin:
		abort(403)

	return render_template('home/passwordgenerator.js', title="Admin Homepage")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
	# prevent non-admins from accessing the page
	if not current_user.is_admin:
		abort(403)

	return render_template('home/admin_dashboard.html', title="Admin Homepage")

@home.route('/client/dashboard.html')
@login_required
def client_dashboard():
	# prevent non-admins from accessing the page
	if not current_user.role_id==2:
		abort(403)

	return render_template('home/client_dashboard.html', title="Client Homepage")

@home.route('/biteam/dashboard.html')
@login_required
def biteam_dashboard():
	# prevent non-admins from accessing the page
	if not current_user.role_id==1:
		abort(403)

	return render_template('home/biteam_dashboard.html', title="BITeam Homepage")
