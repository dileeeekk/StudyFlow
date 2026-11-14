from pathlib import Path
import json,hashlib,shutil

root=Path(__file__).resolve().parent
target=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res')
before=json.loads((root/'before.json').read_text(encoding='utf-8'))
files=list((root/'res').rglob('*.xml'))
for src in files:
    rel=src.relative_to(root/'res'); dst=target/rel
    if dst.exists():
        assert hashlib.sha256(dst.read_bytes()).hexdigest()==before.get(str(rel)), f'File changed: {rel}'
    else: assert str(rel) not in before
for src in files:
    rel=src.relative_to(root/'res'); dst=target/rel
    if dst.exists():
        backup=root/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,backup)
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
print('Installed four launcher icon resources; originals backed up.')
