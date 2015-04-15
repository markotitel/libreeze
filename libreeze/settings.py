"""
Django settings for libreeze project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from os.path import expanduser

home = expanduser("~")

# Load properties from environment
properties = {}
with open(home + '/libreeze.properties', 'r') as properties_file:
    for line in properties_file:
        line = line.rstrip() #removes trailing whitespace and '\n' chars

        if "=" not in line: continue #skips blanks and comments w/o =
        if line.startswith("#"): continue #skips comments which contain =

        key, value = line.split("=", 1)
        properties[key] = value

production = properties['production'] == 'True'

print 'production: ' + production

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = properties['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not production

TEMPLATE_DEBUG = not production

if production:
    ALLOWED_HOSTS = ['.libreeze.net']
else:
    ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'libreeze.urls'

WSGI_APPLICATION = 'libreeze.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#SECURE_BROWSER_XSS_FILTER=True
#SECURE_CONTENT_TYPE_NOSNIFF=True
#SESSION_COOKIE_SECURE=True
#X_FRAME_OPTIONS='DENY'
#CSRF_COOKIE_SECURE=True
#CSRF_COOKIE_HTTPONLY=True
#SECURE_SSL_REDIRECT=True
#SECURE_HSTS_SECONDS=3600
#SECURE_HSTS_INCLUDE_SUBDOMAINS=True

if production:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': properties['mysql_db_name'],
            'USER': properties['mysql_username'],
            'PASSWORD': properties['mysql_password'],
            'HOST': properties['mysql_host'],
            'PORT': properties['mysql_port'],
        }
    }
else:
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = False

#Email
if production:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = properties['smtp_host']
    EMAIL_HOST_USER = properties['smtp_username']
    EMAIL_HOST_PASSWORD = properties['smtp_password']
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

EMAIL_PORT = properties['smtp_port']
EMAIL_USE_SSL = False



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
