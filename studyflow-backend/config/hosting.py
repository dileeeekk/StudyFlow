"""PythonAnywhere deployment; local development continues to use settings.py."""
import json
import os
import re
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

HOSTING_CONFIG = Path(os.environ.get(
    'STUDYFLOW_HOSTING_CONFIG', str(Path.home() / '.studyflow' / 'server.json')))
try:
    _hosting = json.loads(HOSTING_CONFIG.read_text(encoding='utf-8'))
except (OSError, ValueError) as exc:
    raise ImproperlyConfigured('Run setup_hosting.py on the hosting account first.') from exc

_host = _hosting.get('hostname', '')
if not re.fullmatch(r'[a-z0-9][a-z0-9-]*\.(?:eu\.)?pythonanywhere\.com', _host):
    raise ImproperlyConfigured('A specific PythonAnywhere hostname is required.')
for _key in ('DJANGO_SECRET_KEY', 'JWT_SIGNING_KEY'):
    _value = _hosting.get(_key)
    if not isinstance(_value, str) or len(_value) < 50:
        raise ImproperlyConfigured('Hosting signing keys are missing or too short.')
    os.environ[_key] = _value
os.environ['DJANGO_DEBUG'] = '0'
os.environ['DJANGO_ALLOWED_HOSTS'] = _host

from .settings import *  # noqa: E402,F403

# Keep accounts outside the uploaded source folder across code updates.
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': HOSTING_CONFIG.parent / 'db.sqlite3',
    'OPTIONS': {'timeout': 20},
}}
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
CSRF_TRUSTED_ORIGINS = ['https://' + _host]
CACHES = {'default': {
    'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    'LOCATION': 'studyflow_cache',
}}
# PythonAnywhere supplies the request scheme through WSGI. Do not trust
# arbitrary client-supplied X-Forwarded-Proto headers.
SECURE_PROXY_SSL_HEADER = None
