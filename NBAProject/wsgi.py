"""
WSGI config for NBAProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/ubuntu/NBAWebPredictor/NBAProject')

sys.path.append('/home/ubuntu/.local/lib/python3.10/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NBAProject.settings')

application = get_wsgi_application()
