"""
WSGI config for indoor_plant project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the Python path
path = '/home/nevus/Indoor-Plant'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "indoor_plant.settings")

application = get_wsgi_application()
