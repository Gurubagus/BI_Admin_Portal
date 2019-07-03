########################## Imports ################################################################

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required 
from werkzeug.utils import secure_filename
from . import api
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
from collections import OrderedDict

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

@api.route('/api', methods=['GET','POST'])
@login_required
def api_request():
	
	check_BI_permission()

	form1=APIGetInfo(request.form)
	form2=APIXRM(request.form)
	form3=APIFileCopier(request.form)
	
	if request.method =="POST" and form1.company1.data:
		
		api = "http://80.88.187.171:8080/admin-api/get_company?apikey=b3n3c10ud&company="
		c = form1.company1.data
		r = requests.get(api + c)
		p =(r.status_code, r.reason)
		t =(r.text)
		
		return render_template('api/apicall.html',form1=form1,form2=form2,form3=form3,t=t,p=p,
						   title='API Call')

		
	if request.method =="POST" and form3.company3.data:

		api = "http://80.88.187.171:8080/admin-api/create_qv_environment?apikey=b3n3c10ud&app="
		app = form3.app.data.string
		c = form3.company3.data
		r = requests.get(api + app + '&company=' + c)
		p =(r.status_code, r.reason)
		t =(r.text)
		
		return render_template('api/apicall.html',form1=form1,form2=form2,form3=form3,t=t,p=p,
						   title='API Call')

	if request.method =="POST" and form2.company2.data:
		api = "http://80.88.187.171:8080/admin-api/get_xrm_id?apikey=b3n3c10ud&company="
		c = form2.company2.data
		r = requests.get(api + c)
		#p =(r.status_code, r.reason)
		p =(r.reason)
		t =(r.text)
		
		return render_template('api/apicall.html',form1=form1,form2=form2,form3=form3,t=t,p=p,
						   title='API Call')

	return render_template('api/apicall.html',form1=form1,form2=form2,form3=form3,
						   title='API Call')	
	
	