"""
WSGI config for EstLan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

# TODO: will we need to add EstLan to sys.path here?

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
