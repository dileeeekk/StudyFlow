"""Copy this file's contents into the WSGI configuration on the Web tab."""
import os
import sys
from pathlib import Path

project = str(Path.home() / 'studyflow-backend')
if project not in sys.path:
    sys.path.insert(0, project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.hosting'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
