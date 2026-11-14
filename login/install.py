from pathlib import Path
import hashlib,json,shutil
HERE=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
baseline=json.loads((HERE/'before.json').read_text())
for src in (HERE/'StudyFlowApp-login').rglob('*'):
    if not src.is_file(): continue
    rel=src.relative_to(HERE/'StudyFlowApp-login');dest=PROJECT/rel
    if dest.exists():
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==baseline[str(rel)], f'Changed since read: {rel}'
        backup=HERE/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,backup)
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
print('Installed Login files; previous versions backed up.')
