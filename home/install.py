from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
STAGE=ROOT/'StudyFlowApp-home'
before=json.loads((ROOT/'before.json').read_text())
files=[p for p in STAGE.rglob('*') if p.is_file()]
for src in files:
    rel=src.relative_to(STAGE);dest=PROJECT/rel
    if str(rel) in before:assert hashlib.sha256(dest.read_bytes()).hexdigest()==before[str(rel)],str(rel)
    else:assert not dest.exists(),str(rel)
for src in files:
    rel=src.relative_to(STAGE);dest=PROJECT/rel
    if dest.exists():
        backup=ROOT/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,backup)
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
print(f'Installed {len(files)} files; existing versions backed up.')
