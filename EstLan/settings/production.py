from settings.base import *

try:
    from local_settings import *
except ImportError:
    pass


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    'estlan.eu',
    'demo.th3f0x.com', # TODO: Once moved to real domain
]

SEND_EMAIL = False

LOGGING['handlers'] = {
    'info_log': {
        'class': 'logging.handlers.WatchedFileHandler',
        'level': 'INFO',
        'filename': '/var/log/EstLan/info.log',
        'formatter': 'default',
    },
    'error_log': {
        'class': 'logging.handlers.WatchedFileHandler',
        'level': 'ERROR',
        'filename': '/var/log/EstLan/error.log',
        'formatter': 'default',
    },
    'mail_admins': {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'django.utils.log.AdminEmailHandler',
        'formatter': 'default',
    },
}
LOGGING['loggers'][''] = {
    'handlers': ['info_log', 'error_log', 'mail_admins'],
    'level': 'INFO',
    'filters': ['require_debug_false'],
}
