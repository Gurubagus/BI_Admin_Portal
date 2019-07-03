########################## Imports ################################################################

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required 
from werkzeug.utils import secure_filename
from . import qlik_add
from forms import *
from .. import db
from ..models import *
import datetime
import sys
sys.path.append("/home/benemenadmin/PyResources")
from gpconnect import GP_Connect, Timestamp_Update, Log_Table, Qlik_Connect
import uuid

from websocket import create_connection
import psycopg2


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

########################## API Views ################################################################

@qlik_add.route('/qlik_add_user', methods=['GET','POST'])
@login_required
def qlik_add_company():

	check_BI_permission()

	uid=str(uuid.uuid4())
	form=ChooseCompany(request.form)
	#gp = GP_Connect()
	
	if request.method == 'POST':
		s=str(form.formal.data)
		stripped = ''.join(s.split()).lower()
		email = str(stripped+".training@benemen.com")
		#gp = GP_Connect()
		greenplum = psycopg2.connect(host="80.88.187.33", database='BeneDW', user="pyreloader", password="84FsLq?d")
		gp_cursor = greenplum.cursor()
		try:
			gp_cursor.execute("INSERT INTO qlik_sense.qlik_customer_admin_users_attributes SELECT DISTINCT '"+uid+"' as userid, type, value FROM dw.v_qlik_manageruserattributes WHERE userid IN(SELECT userid FROM dw.v_qlik_manageruserattributes WHERE type ='company' AND value='"+form.company.data+"') AND type !='email';")
			gp_cursor.execute("INSERT INTO qlik_sense.qlik_customer_admin_users VALUES ('"+uid+"','"+form.formal.data+"');")
			gp_cursor.execute("INSERT INTO qlik_sense.qlik_customer_admin_users_attributes VALUES('"+uid+"','email','"+email+"');")
			greenplum.commit()
			greenplum.close()
			flash("User: "+form.formal.data+" for "+form.company.data+" has been created.")
			flash("Login UUID: '"+uid+"'")
			flash("(please save for UUID login, it will not be displayed again.)")
		except Exception as e:
			print(e)
			
		return render_template('qlik_add/qlik_add.html',form=form,title='Create Test User')

	return render_template('qlik_add/qlik_add.html',form=form, title='Qlik Add Test User')	
	
	