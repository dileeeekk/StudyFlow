"""Create private local development keys once. Never print them or ship them to Android."""
import json
import secrets
from pathlib import Path

path = Path(__file__).resolve().parent / '.local-settings.json'
if not path.exists():
    with path.open('x', encoding='utf-8') as stream:
        json.dump({'SECRET_KEY': secrets.token_urlsafe(64),
                   'JWT_SIGNING_KEY': secrets.token_urlsafe(64)}, stream)
    print('Local development keys created (excluded from Git).')
else:
    print('Existing local keys preserved.')

