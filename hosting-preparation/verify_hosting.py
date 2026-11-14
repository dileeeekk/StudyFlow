"""Exercise hosting settings with temporary data, never the user's database."""
from pathlib import Path
import json, os, subprocess, tempfile, hashlib

root = Path(__file__).resolve().parent
backend = root.parent / 'studyflow-backend'
python = backend / '.venv/Scripts/python.exe'
existing = {name: hashlib.sha256((backend/name).read_bytes()).hexdigest()
            for name in ('db.sqlite3', '.local-settings.json')}

with tempfile.TemporaryDirectory(prefix='studyflow-hosting-') as folder:
    config = Path(folder)/'server.json'
    env = dict(os.environ, STUDYFLOW_HOSTING_CONFIG=str(config))
    def run(*args):
        result = subprocess.run([str(python), *args], cwd=backend, env=env,
                                capture_output=True, text=True, encoding='utf-8')
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        print(result.stdout.strip())
        if result.stderr.strip(): print(result.stderr.strip())
    run('setup_hosting.py', 'studyflow-test.pythonanywhere.com', '--config', str(config))
    first = config.read_bytes()
    run('setup_hosting.py', 'studyflow-test.pythonanywhere.com', '--config', str(config))
    assert config.read_bytes() == first
    run('manage_hosting.py', 'check', '--deploy', '--fail-level', 'WARNING')
    run('manage_hosting.py', 'migrate', '--noinput', '--verbosity', '0')
    run('manage_hosting.py', 'createcachetable', '--verbosity', '0')
    run('-c', '''import os
os.environ['DJANGO_SETTINGS_MODULE']='config.hosting'
import django;django.setup()
from django.conf import settings
from django.test import Client
assert not settings.DEBUG
client=Client(HTTP_HOST='studyflow-test.pythonanywhere.com')
assert client.get('/api/health/').status_code==301
assert client.get('/api/health/',secure=True).json()=={'status':'ok'}
assert client.get('/api/auth/me/',secure=True).status_code==401
data={'email':'hosting-test@example.com','full_name':'Hosting Test','university':'Test University','password':'Orbit!9StudyCloud72','terms_accepted':True}
response=client.post('/api/auth/register/',data,content_type='application/json',secure=True)
assert response.status_code==201,response.status_code
pair=response.json()
assert client.get('/api/auth/me/',secure=True,HTTP_AUTHORIZATION='Bearer '+pair['access']).status_code==200
refreshed=client.post('/api/auth/refresh/',{'refresh':pair['refresh']},content_type='application/json',secure=True)
assert refreshed.status_code==200
assert client.post('/api/auth/refresh/',{'refresh':pair['refresh']},content_type='application/json',secure=True).status_code==401
assert client.post('/api/auth/logout/',{'refresh':refreshed.json()['refresh']},content_type='application/json',secure=True).status_code==200
assert client.post('/api/auth/refresh/',{'refresh':refreshed.json()['refresh']},content_type='application/json',secure=True).status_code==401
for _ in range(10):
    r=client.post('/api/auth/login/',{'email':'missing@example.com','password':'Wrong!9Password'},content_type='application/json',secure=True)
    assert r.status_code==401
assert client.post('/api/auth/login/',{'email':'missing@example.com','password':'Wrong!9Password'},content_type='application/json',secure=True).status_code==429
print('Hosting smoke test passed: HTTPS, database, JWT rotation/logout, shared throttle cache.')
''')

assert all(hashlib.sha256((backend/name).read_bytes()).hexdigest()==digest for name,digest in existing.items())
print('Local user database and signing keys unchanged.')
