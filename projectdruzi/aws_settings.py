# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['druzi.elestudiodelpintor.com']

DATABASES = { 'default' : { 
	'ENGINE' : 'django.db.backends.mysql',
	'NAME' : 'druzi',
	'USER' : 'druzi',
	'PASSWORD' : 'temporal12',
	'HOST' : 'localhost'
	} 
}
