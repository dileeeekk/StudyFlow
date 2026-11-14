"""Create private hosting configuration once; never rotate existing keys."""
import argparse
import json
import os
from pathlib import Path
import re
import secrets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='Your exact username.pythonanywhere.com hostname')
    parser.add_argument('--config', type=Path, default=Path.home() / '.studyflow' / 'server.json')
    args = parser.parse_args()
    hostname = args.hostname.lower().strip()
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*\.(?:eu\.)?pythonanywhere\.com', hostname):
        parser.error('Enter the hostname only, without https:// or a path.')
    if args.config.exists():
        data = json.loads(args.config.read_text(encoding='utf-8'))
        if data.get('hostname') != hostname:
            parser.error('Existing configuration belongs to another hostname; it was not changed.')
        print('Existing hosting configuration preserved. Signing keys unchanged.')
        return
    args.config.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    data = {'hostname': hostname, 'DJANGO_SECRET_KEY': secrets.token_urlsafe(64),
            'JWT_SIGNING_KEY': secrets.token_urlsafe(64)}
    fd = os.open(args.config, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        json.dump(data, stream)
    print('Private hosting configuration created. Keys are not printed.')


if __name__ == '__main__':
    main()
