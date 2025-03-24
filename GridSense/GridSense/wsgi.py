"""
WSGI config for GridSense project. # Project name updated

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application # Correct import here

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GridSense.settings') # Updated to GridSense.settings

application = get_wsgi_application() # Use get_wsgi_application here