from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
before=json.loads((ROOT/'before.json').read_text())
files=[p for p in (ROOT/'android').rglob('*') if p.is_file()]
for src in files:
    rel=src.relative_to(ROOT/'android');dest=PROJECT/rel
    if str(rel) in before:assert hashlib.sha256(dest.read_bytes()).hexdigest()==before[str(rel)],str(rel)
    else:assert not dest.exists(),str(rel)
for src in files:
    rel=src.relative_to(ROOT/'android');dest=PROJECT/rel
    if dest.exists():
        backup=ROOT/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,backup)
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
print(f'Installed {len(files)} files. Backups saved.')
