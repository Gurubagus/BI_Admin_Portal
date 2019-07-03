from flask import Flask, abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required 
from werkzeug.utils import secure_filename
from . import dkron
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
import shutil

to_upload=""

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

########################## Dkron Views #######################################################

UPLOAD_FOLDER = '/home/benemenadmin/dkron_jobs/python/'
ALLOWED_EXTENSIONS = set(['py'])

@dkron.route('/dkron', methods=['GET','POST'])
@login_required
def dkron_job():
	
	global to_upload
	
	check_BI_permission()
	
	dkron = Dkron.query.all()
	form=DkronJobForm()
	null = None
	
	if form.validate_on_submit():
		
		upload_file()
			
	return render_template('dkron/dkron.html',form=form, dkron=dkron,
						   title='Dkron')
	
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dkron.route('/upload', methods=['GET', 'POST'])
def upload_file():
	
	dkron = Dkron.query.all()
	form=DkronJobForm()
	null = None
	
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect("{{ url_for('dkron.dkron_job'}}")
		file = request.files['file']
		
		if file and allowed_file(file.filename):
			
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			dkron_submit(filename, form)
		
	#return render_template('dkron/dkron.html',form=form, dkron=dkron,
	#					   title='Dkron')
	return redirect(url_for('dkron.dkron_job'))

def make_json(form, name):
	
	try:
		os.chdir("../../dkron_jobs/json")
		if len(form.tags.data)==0:
			   tags = None
		else:
			   tags=form.tags.data
				
		#creating json file from WTForm
		null = None
		
		job = {"name": name,
			   "timezone": form.timezone.data.name,
			   "shell": True, 
			   "schedule": form.schedule.data,
			   "environment_variables": null,
			   "command":"",
			   "owner": form.owner.data,
			   "owner_email": form.owner_email.data,
			   "disabled": form.disable.data,
			   "tags": tags,
			   "retries": form.retries.data,
			   "dependent_jobs": null,
			   "last_success":"0001-01-01T00:00:00Z",
			   "last_error":"0001-01-01T00:00:00Z",
			   "success_count":0,
			   "error_count":0,
			   "parent_job": "",
			   "processors": null,
			   "concurrency": "forbid",
			   "executor": form.executor.data,
			   "executor_config": {"command": "bash /home/benemenadmin/dkron_jobs/bash/"+name+".sh"}}

		with open(str(name) + '.json', 'w') as outfile:
			json.dump(job, outfile, ensure_ascii=False)
		
		return True
	
	except Exception as e:
		
		print('could not create json file due to:')
		print (e.message)

def make_bash(name):
	
	try:
		os.chdir("../../dkron_jobs/bash")
		with open(name + ".sh", "a+") as bash_file:
			bash_file.write("#!/bin/sh\n\ncd ~/dkron_jobs/python\npython3 "+ name + ".py")
		return True
	
	except Exception as e:
		
		print('could not create bash file object due to:')
		print (e.message)
	
def submit_to_bapdb(name, form):	
	
	try:
		cc="allow"
		new_job = Dkron(name=name, 
						timezone = form.timezone.data.name, 
						schedule = form.schedule.data,
						owner = form.owner.data,
						owner_email = form.owner_email.data,
						disabled = form.disable.data,
						tags = form.tags.data,
						retries = form.retries.data,
						concurrency = cc,
						executor = form.executor.data,
						exec_command = "bash /home/benemenadmin/dkron_jobs/bash/"+name+".sh",
						exec_shell = form.exec_shell.data)
		try:	
			db.session.merge(new_job)
			db.session.commit()
			return True
		
		except Exception as e:

			print('could not upload to bapdb due to:')
			print (e.message)
	
	except Exception as e:
		
		print('could not create database object due to:')
		print (e.message)

def upload_to_Dkron(name):
	
	try:
		os.chdir("/home/benemenadmin/dkron_jobs/json")
		os.system("python JOBPOST_dkron.py "+ name +".json")
		
		return True
	
	except Exception as e:
		
		print('could not upload to Dkron due to:')
		print (e.message)
	
def dkron_submit(filename, form):
	
	
	name = os.path.splitext(filename)
	name = str(name[0])
	
	try:
		make_json(form, name)
		make_bash(name)
		submit_to_bapdb(name, form)
		upload_to_Dkron(name)
		
	
	except Exception as e:
		
		print('Error in create/upload methods (json,bash,bapdb,Dkron) error as follows:')
		print (e.message)
	
	finally:
	
		return True
		"""
		dkron = Dkron.query.all()
		form=DkronJobForm()
		null = None
		
		return render_template('dkron/dkron.html', form=form,
						   title='Dkron')
		"""	
		
def delete_json(name):
	
	os.chdir("/home/benemenadmin/dkron_jobs/json")
	os.rename("/home/benemenadmin/dkron_jobs/json/"+name+".json", "/home/benemenadmin/dkron_jobs/removed_jobs/json/"+name+".json")
	#os.remove(name + ".json")
	
	
def delete_bash(name):
	
	os.chdir("/home/benemenadmin/dkron_jobs/bash")
	os.remove(name + ".sh")
	
def delete_python(name):
	
	os.chdir("/home/benemenadmin/dkron_jobs/python")
	os.rename("/home/benemenadmin/dkron_jobs/python/"+name+".py", "/home/benemenadmin/dkron_jobs/removed_jobs/python/"+name+".py")
	#os.remove(name + ".py")

def remove_from_dkron(name):
	
	try:
		os.chdir("../../dkron_jobs/json")
		os.system("python JOBDELETE_dkron.py "+ name)
		
		return True
	
	except Exception as e:
		
		print('could not delete from Dkron due to:')
		print (e.message)
	
@dkron.route('/dkron/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_dkron(id):
	"""
	Delete an Dkron job from the database
	"""
	check_BI_permission()
	
	job = Dkron.query.get_or_404(id)
	name = job.name
	
	try:
		db.session.delete(job)
		db.session.commit()
		
		delete_json(name)
		delete_bash(name)
		delete_python(name)
		remove_from_dkron(name)
		flash('You have successfully deleted '+name+' from Dkron.')

		return redirect(url_for('dkron.dkron_job'))

	except Exception as e:
		#flash('Sorry, and error has occurred during the deletion attempt.') 
		flash(e.message)
		return redirect(url_for('dkron.dkron_job'))
	
	return render_template('dkron/dkron.html',
						   title='Dkron Delete')

class JobChange():
	
	def __init__(self, name, upordown):
		
		self.job = str(name)
		self.upordown = upordown
		
		self.choose_path(self.job, self.upordown)
	
	def choose_path(self, job, updordown):
	
		try:
			if self.upordown == '+':
				self.bap_db_activate(job)

			elif self.upordown == '-':
				self.bap_db_deactivate(job)
			
		except Exception as e:
			print (e.message)
			
			
	def upload_to_Dkron(self, name):
	
		try:
			os.chdir("/home/benemenadmin/dkron_jobs/json")
			os.system("python JOBPOST_dkron.py "+ name +".json")

			return True

		except Exception as e:

			print('could not upload to Dkron due to:')
			print (e.message)
			
	def bap_db_activate(self, job):
		
		try:
			job = Dkron.query.get_or_404(job)
			job.disabled=False
			db.session.commit()
			self.dkron_activate(job)
		
		except Exception as e:
			print (e.message)
			
	
	def bap_db_deactivate(self, job):
		
		try:
			job = Dkron.query.get_or_404(job)
			job.disabled=True
			db.session.commit()
			self.dkron_deactivate(job)
			
		except Exception as e:

			print (e.message)
		
	
	def change_json_submit(self, job, change):
		
		try:
			#creating json file from WTForm
			null = None
			os.chdir("../../dkron_jobs/json")
			if len(job.tags)==0:
				tags = None
			else:
			   	tags=job.tags
			
			upload = {"name": job.name,
				   "timezone": job.timezone,
				   "shell": True, 
				   "schedule": job.schedule,
				   "environment_variables": null,
				   "command":"",
				   "owner": job.owner,
				   "owner_email": job.owner_email,
				   "disabled": change,
				   "tags": tags,
				   "retries": job.retries,
				   "dependent_jobs": null,
				   "last_success":"0001-01-01T00:00:00Z",
				   "last_error":"0001-01-01T00:00:00Z",
				   "success_count":0,
				   "error_count":0,
				   "parent_job": "",
				   "processors": null,
				   "concurrency": "forbid",
				   "executor": job.executor,
				   "executor_config": {"command": "bash /home/benemenadmin/dkron_jobs/bash/"+job.name+".sh"}}

			with open(str(job.name) + '.json', 'w') as outfile:
				json.dump(upload, outfile, ensure_ascii=False)
			
			name = str(job.name)
			self.upload_to_Dkron(name)
			
		except Exception as e:

			print('could not create json file due to:')
			print (e.message)
	
	def dkron_activate(self, job):
		
		change = False
		self.change_json_submit(job, change)
		
	def dkron_deactivate(self, job):
		
		change = True
		self.change_json_submit(job, change)


@dkron.route('/dkron/activate/<name>', methods=['GET', 'POST'])
@login_required
def activate_dkron_job(name):
	
	check_admin()
	
	try:
		JobChange(name, upordown = '+')
		flash('You have successfully activated the job.')
	
	except Exception as e:

			print (e.message)

	
	# redirect to the db connection page
	return redirect(url_for('dkron.dkron_job'))

@dkron.route('/dkron/deactivate/<name>', methods=['GET', 'POST'])
@login_required
def deactivate_dkron_job(name):
	
	check_admin()
	
	try:
		JobChange(name, upordown = '-')
		flash('You have successfully deactivated the job.')
	
	except Exception as e:

			print (e.message)
			
	# redirect to the db connection page
	return redirect(url_for('dkron.dkron_job'))