from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
before=json.loads((ROOT/'before.json').read_text())
for src in (ROOT/'StudyFlowApp-register').rglob('*'):
    if not src.is_file():continue
    rel=src.relative_to(ROOT/'StudyFlowApp-register');dest=PROJECT/rel
    if dest.exists():
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==before[str(rel)],str(rel)
        backup=ROOT/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,backup)
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
print('Installed Register; existing changed files backed up.')
