class Config(object):
	"""
	Common configurations
	"""

	# Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
	"""
	Development configurations
	"""

	DEBUG = True
	SQLALCHEMY_ECHO = True
	UPLOAD_FOLDER = '/home/benemenadmin/dkron_jobs/python/'


class ProductionConfig(Config):
	"""
	Production configurations
	"""

	DEBUG = False

app_config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'default': ProductionConfig
}
