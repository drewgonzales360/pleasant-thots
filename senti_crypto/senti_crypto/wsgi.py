"""
WSGI config for senti_crypto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import sys, os, thread
from farmer import main

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senti_crypto.settings")

application = get_wsgi_application()

thread.start_new_thread(main.start, ())
