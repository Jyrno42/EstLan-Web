# Django settings for EstLan project.
import os
import sys

# SITE_NAME
SITE_NAME = u'EstLan'
SITE_VERSION = u'0.0.1a'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ADMINS = (
    ('Jyrno Ader', 'jyrno42@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'server.db',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'main_estlan_cache'
    }
}

ALLOWED_HOSTS = [
    'estlan.eu',
    'estlan.th3f0x.com',
]

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'et'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('et', 'Eesti'),
    ('en', 'English (US)'),
)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

ADMIN_MEDIA_PREFIX = os.path.join(STATIC_URL, 'admin/')

SECRET_KEY = 'UNKNOWN'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'utils.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates')
)

INSTALLED_APPS = (
    # Basic django stuff
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Admin tools stuff
    'django.contrib.admin',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    
    # Utilities & stuff
    'social_auth',
    'south',
    'easy_thumbnails',
    'compressor',
    'crispy_forms',
    'dajaxice',
    
    # Apps for EstLan
    'utils',
    'estlan'
)

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s [%(asctime)s] %(module)s %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'dajaxice' : {
            'level': 'WARNING',
        },
    },
}

# Social auth and generic session conf

SESSION_COOKIE_AGE = 604800

'''
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    #'detect_new',
    #'associate_to_email_when_no_socialauth',
    #'associate_to_loggedin_user',
    'social_auth.backends.pipeline.user.get_username',
    #'create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    #'update_new_users_details',
    #'update_fb_extra_data',
    #'update_google_extra_data',
)

SOCIAL_AUTH_DEFAULT_USERNAME = 'custom_sa_auth_user'
SOCIAL_AUTH_SESSION_EXPIRATION = False

AUTH_PROFILE_MODULE = 'account.UserProfile'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
    'account.backends.EmailAuthBackend', # Log in by email:password
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LOGIN_ERROR_URL = '/sc_login_error'
SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

'''

# FACEBOOK & GOOGLE APP

FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''

GOOGLE_OAUTH2_CLIENT_ID = ''
GOOGLE_OAUTH2_CLIENT_SECRET = ''
GOOGLE_DISPLAY_NAME = SITE_NAME

FACEBOOK_EXTENDED_PERMISSIONS = [
    'offline_access', # TODO: Will be removed, find alternative.
    'email',
    'user_about_me',
    'user_birthday',
]

# Django Compressor settings
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.SlimItFilter',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    
    'social_auth.context_processors.social_auth_by_name_backends',
    'django.core.context_processors.request',
]

SEND_EMAIL = False
DEFAULT_FROM_EMAIL = 'info@estlan.eu'
SERVER_EMAIL = 'info@estlan.eu'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_PORT = 587

LOGIN_URL = '/login'

