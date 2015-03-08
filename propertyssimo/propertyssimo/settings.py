"""
Django settings for propertyssimo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a7*n!6+^z7%r00ffo8=2g!ab+1eitiilspb(%2yte#)izee+2='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'listings',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'propertyssimo.urls'

WSGI_APPLICATION = 'propertyssimo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':'propertyssimo',
	'USER':'propertyssimo',
	'PASSWORD':'propertyssimo',
	'HOST':'127.0.0.1',
	'PORT':'5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

DBZ_XML_LINK = 'http://prop-pix.com/cms/issmo_dbz/live/'
PF_XML_LINK = 'http://prop-pix.com/cms/issmo_pf/live_v2/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DOMAIN_NAME = 'http://www.ichdubai.com/'
MEDIA_URL = 'media/'


## Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'prop_pix'
EMAIL_HOST_PASSWORD = 'quakeroats'
DEFAULT_FROM_EMAIL = 'support@prop-pix.com'
SERVER_EMAIL = 'support@prop-pix.com'

WATERMARK = os.path.join(BASE_DIR, 'logo_final.png')
WATERMARK_OPACITY = 0.25

