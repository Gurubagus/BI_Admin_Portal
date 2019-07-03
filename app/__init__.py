# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import flash, redirect, render_template, url_for

# local imports
from config import app_config

UPLOAD_FOLDER='/home/benemenadmin/dkron_jobs/python'
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	app.config['UPLOADED_FOLDER'] = UPLOAD_FOLDER

	Bootstrap(app)
	db.init_app(app)
	login_manager.init_app(app)
	login_manager.login_message = "You must be logged in to access this page."
	login_manager.login_view = "auth.login"
	migrate = Migrate(app, db)

	from app import models

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/admin')

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)
	
	from .dkron import dkron as dkron_blueprint
	app.register_blueprint(dkron_blueprint)
	
	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint)
	
	from .qlik_add import qlik_add as qlik_add_blueprint
	app.register_blueprint(qlik_add_blueprint)
	
	from .db_connections import db_connections as db_connections_blueprint
	app.register_blueprint(db_connections_blueprint)
	
	@app.errorhandler(403)
	def forbidden(error):
		return render_template('errors/403.html', title='Forbidden'), 403

	@app.errorhandler(404)
	def page_not_found(error):
		return render_template('errors/404.html', title='Page Not Found'), 404

	@app.errorhandler(500)
	def internal_server_error(error):
		return render_template('errors/500.html', title='Server Error'), 500

	return app
