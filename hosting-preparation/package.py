from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

root = Path(__file__).resolve().parent
backend = root.parent/'studyflow-backend'
files = [backend/name for name in (
    'manage.py', 'manage_hosting.py', 'setup_hosting.py', 'deploy_pythonanywhere.py',
    'pythonanywhere_wsgi.py', 'requirements.txt', '.gitignore', 'HOSTING.md')]
for folder in ('accounts', 'config', 'planner'):
    files.extend((backend/folder).rglob('*.py'))
archive = root/'StudyFlow-hosting.zip'
with ZipFile(archive, 'w', ZIP_DEFLATED) as output:
    for path in sorted(files):
        assert path.is_file()
        output.write(path, 'studyflow-backend/'+path.relative_to(backend).as_posix())
with ZipFile(archive) as check:
    assert check.testzip() is None
    assert not any(name.endswith(('.sqlite3', '.log', '.json', '.pyc')) for name in check.namelist())
(root/'archive-manifest.json').write_text(json.dumps({
    'archive_files': len(files), 'contains_planner': True,
    'contains_database_or_secrets': False
},indent=2),encoding='utf-8')
print(f'Archive ready: {len(files)} source files; no accounts, tokens or signing keys.')
