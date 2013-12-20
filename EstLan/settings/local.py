from settings.base import *

try:
    from local_settings import *
except ImportError:
    pass

MIDDLEWARE_CLASSES.append(
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS.append(
    'debug_toolbar',
)