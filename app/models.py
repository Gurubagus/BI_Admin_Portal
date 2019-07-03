from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text
from sqlalchemy.orm import relationship, backref
from uuid import uuid4
import datetime

SQLALCHEMY_ECHO = True

class Employee(UserMixin, db.Model):
	"""
	Create an Employee table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	__tablename__ = 'employees'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60))
	username = db.Column(db.String(60))
	first_name = db.Column(db.String(60))
	last_name = db.Column(db.String(60))
	password_hash = db.Column(db.String(128))
	department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	is_admin = db.Column(db.Boolean, default=False)
	modified = db.Column(db.DateTime, onupdate=func.utcnow())

	@property
	def password(self):
		"""
		Prevent pasword from being accessed
		"""
		raise AttributeError('password is not a readable attribute.')

	@password.setter
	def password(self, password):
		"""
		Set password to a hashed password
		"""
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		"""
		Check if hashed password matches actual password
		"""
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
	return Employee.query.get(int(user_id))


class Department(db.Model):
	"""
	Create a Department table
	"""

	__tablename__ = 'departments'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	description = db.Column(db.String(200))
	employees = db.relationship('Employee', backref='department',
								lazy='dynamic')

	def __repr__(self):
		return '<Department: {}>'.format(self.name)


class Role(db.Model):
	"""
	Create a Role table
	"""

	__tablename__ = 'roles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	description = db.Column(db.String(200))
	employees = db.relationship('Employee', backref='role',
								lazy='dynamic')
	modified = db.Column(db.DateTime, onupdate=func.utcnow())
	
	def __repr__(self):
		return '<Role: {}>'.format(self.name)

##################################################################################################
	
class Organization(db.Model):
	"""
	Create an Organization table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'organizations'

	org_key = db.Column(UUID(as_uuid=True), default=uuid4(), primary_key=True) # Index may be an issue
	short_name = db.Column(db.String(60))
	description = db.Column(db.String(255))
	modified = db.Column(db.DateTime, default=func.utcnow(), onupdate=func.now())
	active =db.Column(db.Boolean, default=True)
	
	def __repr__(self):
		return '<Organization: {}>'.format(self.short_name)

	
class Source_Keys(db.Model):
	"""
	Create an Organization table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'source_keys'

	org_key = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.org_key'), primary_key=True, index=True)
	source_key = db.Column(db.String(60), db.ForeignKey('data_sources.source_key'), primary_key=True)
	source_id = db.Column(db.String(60))
	modified = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

	def __repr__(self):
		return '<Source_Keys: {}>'.format(self.source_key)
	
class Data_Source(db.Model):
	"""
	Create an Organization table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'data_sources'

	source_key = db.Column(db.String(60), primary_key=True)
	short_description = db.Column(db.String(60))
	modified = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=func.now())

	def __repr__(self):
		return '<Data_Source: {}>'.format(self.short_description)

class Variable(db.Model):
	"""
	Create all Variables table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'variables'

	variable_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	variable_name = db.Column(db.String(60))
	variable_description = db.Column(db.String(60))
	variable_type = db.Column(db.String(60))
	variable_default = db.Column(db.String(60))
	variable_class = db.Column(db.String(60))
	variable_validator = db.Column(db.String(255))
	children = relationship('Variable_Values')
	modified = db.Column(db.DateTime, default=func.utcnow(), onupdate=func.now())
	
	def __repr__(self):
		return '<Variable: {}>'.format(self.variable_name)

class Variable_Class(db.Model):
	"""
	Create all Variables table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'variable_classes'

	variable_class = db.Column(db.String(60), primary_key=True)
	variable_class_description = db.Column(db.String(60))
	modified = db.Column(db.DateTime, default=func.utcnow(), onupdate=func.now())

	def __repr__(self):
		return '<Variable_Classes: {}>'.format(self.variable_class_description)
	
class Variable_Values(db.Model):
	"""
	Create all values for the variables table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'variable_values'

	variable_id = db.Column(db.Integer, db.ForeignKey('variables.variable_id', ondelete='CASCADE'), primary_key=True, autoincrement=True)
	org_key = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.org_key', ondelete='CASCADE'), primary_key=True)
	var_value = db.Column(db.String(60))
	parent = db.relationship('Organization', backref=backref('Variable_Values', passive_deletes=True))
	modified = db.Column(db.DateTime, default=func.utcnow(), onupdate=func.now())
	
	def __repr__(self):
		return '<Variable: {}>'.format(self.org_key)
	
	
class Report(db.Model):
	"""
	Create Report table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'reports'

	report_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # seqentual
	report_name = db.Column(db.String(60))
	report_description = db.Column(db.String(255))
	modified = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
		
	def __repr__(self):
		return '<Variable: {}>'.format(self.report_name)
	
class Email_list(db.Model):
	"""
	Create Email table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'email_lists'

	email_list_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # sequential
	email_description = db.Column(db.String(255))
	org_key = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.org_key', ondelete='CASCADE'), index=True)
	modified = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
	
	def __repr__(self):
		return '<Variable: {}>'.format(self.email_description)
	
class Email_recipient(db.Model):
	"""
	Create Email table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'email_recipients'

	email_list_id = db.Column(db.Integer, db.ForeignKey('email_lists.email_list_id'), primary_key=True, autoincrement=True)
	email = db.Column(db.String(60),primary_key=True)
	org_key = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.org_key', ondelete='CASCADE'))
	parent = db.relationship('Email_list', backref=backref('Email_recipient', passive_deletes=True))
	modified = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
	
	def __repr__(self):
		return '<Variable: {}>'.format(self.email)
	
	
	
class Report_delivery(db.Model):
	"""
	Create Email table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'report_deliveries'

	org_key = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.org_key'), primary_key=True)
	report_id = db.Column(db.Integer, db.ForeignKey('reports.report_id'),primary_key=True)
	email_list_id = db.Column(db.Integer, db.ForeignKey('email_lists.email_list_id'),primary_key=True)
	filters = db.Column(db.String(255))
	parent = db.relationship('Report', backref=backref('Report_delivery', passive_deletes=True))
	parent = db.relationship('Email_list', backref=backref('Report_delivery', passive_deletes=True))
	modified = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
	
	def __repr__(self):
		return '<Variable: {}>'.format(self.email)

class API(db.Model):
	"""
	Create API table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'apis'

	api_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	string = db.Column(db.String(255))
	modified = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
	
	def __repr__(self):
		return '<API: {}>'.format(self.name)
	
	
class APP(db.Model):
	"""
	Create API table
	"""

	# Ensures table will be named in plural and not in singular
	# as is the name of the model
	
	__tablename__ = 'apps'

	app_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	string = db.Column(db.String(255))
	modified = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
	
	def __repr__(self):
		return '<APP: {}>'.format(self.name)

class Timezone(db.Model):
	
	"""
	List of all timezones for Dkron json creator
	"""
	
	__tablename__ = 'timezones'
	
	timezoneid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100))
	fset = db.Column(db.Integer, default=0)
	offset_dst = db.Column(db.Integer, default=0)
	

class Dkron(db.Model):
	"""
	Storage for all Dkron jobs submitted
	"""
	
	__tablename__='dkrons'
	
	name = db.Column(db.String(60), primary_key=True)
	timezone = db.Column(db.String(100))
	schedule = db.Column(db.String(100))
	owner = db.Column(db.String(100))
	owner_email = db.Column(db.String(100))
	disabled = db.Column(db.Boolean, default=False)
	tags = db.Column(db.String(100))
	retries = db.Column(db.Integer, default=0)
	concurrency =db.Column(db.String(60), default="allow")
	executor =db.Column(db.String(60), default="shell")
	exec_command = db.Column(db.String(250))
	exec_shell = db.Column(db.Boolean, default=True)
	modified = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
	
class Db_connection(db.Model):
	"""
	Storage for all Dkron jobs submitted
	"""
	
	__tablename__='db_connections'
	
	name = db.Column(db.String(100), primary_key=True)
	server = db.Column(db.String(100))
	port = db.Column(db.Integer, default=0)
	database = db.Column(db.String(100))
	login = db.Column(db.String(100))
	password = db.Column(db.String(100))
	additionalparams = db.Column(db.String(100))
	system_type = db.Column(db.String(100))
	active = db.Column(db.Boolean, default=True)
	