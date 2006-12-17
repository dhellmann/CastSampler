# Django settings for CastSampler project.
#
# $Id$
#

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import logging
if DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO
logging.basicConfig(filename='/tmp/castsampler.log',
                    filemode='w',
                    level=level,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    )

#
# Configure the trace module to write trace messages to the log file.
#
if DEBUG:
    from trace import trace, LogOutput
    trace.setOutputStream(LogOutput())
    

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Doug Hellmann', 'doug@hellfly.net'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = '/Users/dhellmann/Devel/CastSampler/src/trunk/CastSampler/db/castsampler.db' # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#q1-kil!)n+@wy!*a_oef^!&3))0=#sp_fk%u!8837#2v6h%xa'

# Set up user registration profile model
#AUTH_PROFILE_MODULE = 'CastSampler.registration.models'

SITE_NAME = 'CastSampler'

# Outgoing email for user registration
EMAIL_HOST = 'smtp'
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
DEFAULT_FROM_EMAIL = 'castsampler@gmail.com'
SERVER_EMAIL = 'doug-castsampler@hellfly.net'

#EMAIL_PORT = 25

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'CastSampler.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/Users/dhellmann/Devel/CastSampler/src/trunk/CastSampler/templates',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'CastSampler.oneoffcast',
    'CastSampler.registration',
)
