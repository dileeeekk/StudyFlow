"""Run inside the hosting virtualenv after uploading the source archive."""
import argparse
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
args = parser.parse_args()
root = Path(__file__).resolve().parent
commands = [
    ['setup_hosting.py', args.hostname],
    ['manage_hosting.py', 'check', '--deploy', '--fail-level', 'WARNING'],
    ['manage_hosting.py', 'migrate', '--noinput'],
    ['manage_hosting.py', 'createcachetable'],
    ['manage_hosting.py', 'collectstatic', '--noinput'],
]
for command in commands:
    subprocess.run([sys.executable, *command], cwd=root, check=True)
print('Ready for the Web tab: Manual configuration, same Python version and virtualenv.')
print('WSGI template: pythonanywhere_wsgi.py; static URL: /static/; folder:', root/'staticfiles')
