# Parse database configuration from $DATABASE_URL
import dj_database_url

DATABASES = { 'default' : { 
	'ENGINE' : 'django.db.backends.mysql', 
	'AUTOCOMMIT' : False ,
	'NAME' : 'druzi',
	'USER' : 'druzi',
	'PASSWORD' : 'temporal12',
	'HOST' : 'localhost'
	} 
}
