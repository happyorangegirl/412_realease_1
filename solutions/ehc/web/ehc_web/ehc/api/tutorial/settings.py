# Django settings for tutorial project.

BDL_CONFIG_FILE = 'var/lc1s.json'
EHC_CONFIG = {
    '1':'/root/automation/ehc/config/E2EWF-1-LC1S.config.yaml',
    '2':'/root/automation/ehc/config/E2EWF-1-CA1S.config.yaml',
    '3':'/root/automation/ehc/config/E2EWF-1-CA2S.config.yaml',
    '4':'/root/automation/ehc/config/E2EWF-1-DR2S.config.yaml',
    '5':'/root/automation/ehc/config/E2EWF-1-MP2S.config.yaml',
    '6':'/root/automation/ehc/config/E2EWF-1-MP3S.config.yaml',
    '7':'/root/automation/ehc/config/E2EWF-1-VS1S.config.yaml',
    '8':'/root/automation/ehc/config/E2EWF-2-LC1S.config.yaml',
    '9':'/root/automation/ehc/config/E2EWF-2-CA1S.config.yaml',
    '10':'/root/automation/ehc/config/E2EWF-2-CA2S.config.yaml',
    '11':'/root/automation/ehc/config/E2EWF-2-DR2S.config.yaml',
    '12':'/root/automation/ehc/config/E2EWF-2-MP2S.config.yaml',
    '13':'/root/automation/ehc/config/E2EWF-2-MP3S.config.yaml',
    '14':'/root/automation/ehc/config/E2EWF-2-VS1S.config.yaml',
    '15':'/root/automation/ehc/config/E2EWF-3-LC1S.config.yaml',
    '16':'/root/automation/ehc/config/E2EWF-3-CA1S.config.yaml',
    '17':'/root/automation/ehc/config/E2EWF-3-CA2S.config.yaml',
    '18':'/root/automation/ehc/config/E2EWF-3-DR2S.config.yaml',
    '19':'/root/automation/ehc/config/E2EWF-3-MP2S.config.yaml',
    '20':'/root/automation/ehc/config/E2EWF-3-MP3S.config.yaml',
    '21':'/root/automation/ehc/config/E2EWF-3-VS1S.config.yaml',
    '22':'/root/automation/ehc/config/E2EWF-4-LC1S.config.yaml',
    '23':'/root/automation/ehc/config/E2EWF-4-CA1S.config.yaml',
    '24':'/root/automation/ehc/config/E2EWF-4-CA2S.config.yaml',
    '25':'/root/automation/ehc/config/E2EWF-4-DR2S.config.yaml',
    '26':'/root/automation/ehc/config/E2EWF-4-MP2S.config.yaml',
    '27':'/root/automation/ehc/config/E2EWF-4-MP3S.config.yaml',
    '28':'/root/automation/ehc/config/E2EWF-4-VS1S.config.yaml',
    '30':'/root/automation/ehc/config/E2EWF-7-C1-LC1S.config.yaml',
    '31':'/root/automation/ehc/config/E2EWF-7-C2-CA1S.config.yaml',
    '32':'/root/automation/ehc/config/E2EWF-7-C3-CA2S.config.yaml',
    '33':'/root/automation/ehc/config/E2EWF-7-C4-DR2S.config.yaml',
    '34':'/root/automation/ehc/config/E2EWF-7-C5-MP2S.config.yaml',
    '35':'/root/automation/ehc/config/E2EWF-7-C6-MP3S.config.yaml',
    '36':'/root/automation/ehc/config/E2EWF-7-C7-RP4VM.config.yaml',
    '37':'/root/automation/ehc/config/E2EWF-7-C8-VS1S.config.yaml',
    '38':'/root/automation/ehc/config/E2EWF-10.config.yaml',
    '39':'/root/automation/ehc/config/E2EWF-8-C3-CA2S.config.yaml',
    '42':'/root/automation/ehc/config/E2EWF-9-C4-DR2S.config.yaml',
    '43':'/root/automation/ehc/config/E2EWF-9-C5-MP2S.config.yaml',
    '44':'/root/automation/ehc/config/E2EWF-9-C6-MP3S.config.yaml',
    '45':'/root/automation/ehc/config/E2EWF-101-RP4VM.config.yaml',
    '46':'/root/automation/ehc/config/E2EWF-102-RP4VM-DP.config.yaml',
    '47':'/root/automation/ehc/config/E2EWF-101-C8-RP4VM.config.yaml',
    '48':'/root/automation/ehc/config/scenario_conf/E2ESN-1-DR2S.config.yaml',
    '49':'/root/automation/ehc/config/scenario_conf/E2ESN-1-LC1S.config.yaml',
    '50':'/root/automation/ehc/config/scenario_conf/E2ESN-1-RP4VM.config.yaml',
    '51':'/root/automation/ehc/config/scenario_conf/E2ESN-3-RP4VM.config.yaml',
    '52':'/root/automation/ehc/config/scenario_conf/E2ESN-3-LC1S.config.yaml',
    '53':'/root/automation/ehc/config/scenario_conf/E2ESN-4-BASIC-DR2S.config.yaml',
    '54':'/root/automation/ehc/config/scenario_conf/E2ESN-4-ADDITIONAL-DR2S.config.yaml',
    '55':'/root/automation/ehc/config/scenario_conf/E2ESN-1-CA2S.config.yaml',
    '56':'/root/automation/ehc/config/scenario_conf/E2ESN-1-CA1S.config.yaml',
    '57': '/root/automation/ehc/config/scenario_conf/E2ESN-2-RP4VM.config.yaml',
    '0':'/root/automation/ehc/config/generic.yaml'
}

EHC_CONFIG_SCHEMA = {
    '/root/automation/ehc/schema/web/generic.yaml.json':'0',
    '/root/automation/ehc/schema/web/E2EWF-1-LC1S.config.yaml.json':'1',
    '/root/automation/ehc/schema/web/E2EWF-1-CA1S.config.yaml.json':'2',
    '/root/automation/ehc/schema/web/E2EWF-1-CA2S.config.yaml.json':'3',
    '/root/automation/ehc/schema/web/E2EWF-1-DR2S.config.yaml.json':'4',
    '/root/automation/ehc/schema/web/E2EWF-1-MP2S.config.yaml.json':'5',
    '/root/automation/ehc/schema/web/E2EWF-1-MP3S.config.yaml.json':'6',
    '/root/automation/ehc/schema/web/E2EWF-1-VS1S.config.yaml.json':'7',
    '/root/automation/ehc/schema/web/E2EWF-2-LC1S.config.yaml.json':'8',
    '/root/automation/ehc/schema/web/E2EWF-2-CA1S.config.yaml.json':'9',
    '/root/automation/ehc/schema/web/E2EWF-2-CA2S.config.yaml.json':'10',
    '/root/automation/ehc/schema/web/E2EWF-2-DR2S.config.yaml.json':'11',
    '/root/automation/ehc/schema/web/E2EWF-2-MP2S.config.yaml.json':'12',
    '/root/automation/ehc/schema/web/E2EWF-2-MP3S.config.yaml.json':'13',
    '/root/automation/ehc/schema/web/E2EWF-2-VS1S.config.yaml.json':'14',
    '/root/automation/ehc/schema/web/E2EWF-3-LC1S.config.yaml.json':'15',
    '/root/automation/ehc/schema/web/E2EWF-3-CA1S.config.yaml.json':'16',
    '/root/automation/ehc/schema/web/E2EWF-3-CA2S.config.yaml.json':'17',
    '/root/automation/ehc/schema/web/E2EWF-3-DR2S.config.yaml.json':'18',
    '/root/automation/ehc/schema/web/E2EWF-3-MP2S.config.yaml.json':'19',
    '/root/automation/ehc/schema/web/E2EWF-3-MP3S.config.yaml.json':'20',
    '/root/automation/ehc/schema/web/E2EWF-3-VS1S.config.yaml.json':'21',
    '/root/automation/ehc/schema/web/E2EWF-4-LC1S.config.yaml.json':'22',
    '/root/automation/ehc/schema/web/E2EWF-4-CA1S.config.yaml.json':'23',
    '/root/automation/ehc/schema/web/E2EWF-4-CA2S.config.yaml.json':'24',
    '/root/automation/ehc/schema/web/E2EWF-4-DR2S.config.yaml.json':'25',
    '/root/automation/ehc/schema/web/E2EWF-4-MP2S.config.yaml.json':'26',
    '/root/automation/ehc/schema/web/E2EWF-4-MP3S.config.yaml.json':'27',
    '/root/automation/ehc/schema/web/E2EWF-4-VS1S.config.yaml.json':'28',
    '/root/automation/ehc/schema/web/E2EWF-7-C1-LC1S.config.yaml.json':'30',
    '/root/automation/ehc/schema/web/E2EWF-7-C2-CA1S.config.yaml.json':'31',
    '/root/automation/ehc/schema/web/E2EWF-7-C3-CA2S.config.yaml.json':'32',
    '/root/automation/ehc/schema/web/E2EWF-7-C4-DR2S.config.yaml.json':'33',
    '/root/automation/ehc/schema/web/E2EWF-7-C5-MP2S.config.yaml.json':'34',
    '/root/automation/ehc/schema/web/E2EWF-7-C6-MP3S.config.yaml.json':'35',
    '/root/automation/ehc/schema/web/E2EWF-7-C7-RP4VM.config.yaml.json':'36',
    '/root/automation/ehc/schema/web/E2EWF-7-C8-VS1S.config.yaml.json':'37',
    '/root/automation/ehc/schema/web/E2EWF-10.config.yaml.json':'38',
    '/root/automation/ehc/schema/web/E2EWF-8-C3-CA2S.config.yaml.json':'39',
    '/root/automation/ehc/schema/web/E2EWF-9-C4-DR2S.config.yaml.json':'42',
    '/root/automation/ehc/schema/web/E2EWF-9-C5-MP2S.config.yaml.json':'43',
    '/root/automation/ehc/schema/web/E2EWF-9-C6-MP3S.config.yaml.json':'44',
    '/root/automation/ehc/schema/web/E2EWF-101-RP4VM.config.yaml.json':'45',
    '/root/automation/ehc/schema/web/E2EWF-102-RP4VM-DP.config.yaml.json':'46',
    '/root/automation/ehc/schema/web/E2EWF-101-C8-RP4VM.config.yaml.json':'47',
    '/root/automation/ehc/schema/web/E2ESN-1-DR2S.config.yaml.json':'48',
    '/root/automation/ehc/schema/web/E2ESN-1-LC1S.config.yaml.json':'49',
    '/root/automation/ehc/schema/web/E2ESN-1-RP4VM.config.yaml.json':'50',
    '/root/automation/ehc/schema/web/E2ESN-3-RP4VM.config.yaml.json':'51',
    '/root/automation/ehc/schema/web/E2ESN-3-LC1S.config.yaml.json':'52',
    '/root/automation/ehc/schema/web/E2ESN-4-BASIC-DR2S.config.yaml.json':'53',
    '/root/automation/ehc/schema/web/E2ESN-4-ADDITIONAL-DR2S.config.yaml.json':'54',
    '/root/automation/ehc/schema/web/E2ESN-1-CA2S.config.yaml.json':'55',
    '/root/automation/ehc/schema/web/E2ESN-1-CA1S.config.yaml.json':'56',
    '/root/automation/ehc/schema/web/E2ESN-2-RP4VM.config.yaml.json': '57'
}

SELECTED_CONFIG = '/root/automation/ehc/schema/web/generic.yaml.json'
SELECTED_CONFIG_SCHEMA = '/root/automation/ehc/schema/web/generic.yaml.json'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Or use an alternate database backend.
        'NAME': 'tmp.db',                       # Path to sqlite3 database file.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '98s9du5ruv!j%shx0udb#uz1g@v^xl65zm1l-_5%8cs6%c*qm$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'tutorial.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tutorial.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # https://github.com/ottoyiu/django-cors-headers
    'corsheaders',
    # http://www.django-rest-framework.org/
    'rest_framework',
    'snippets',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
}

import os
if os.environ.get('HEROKU'):  # heroku config:set HEROKU=1
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()

LOGIN_REDIRECT_URL = '/'
