from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
before=json.loads((ROOT/'before.json').read_text())
for src in (ROOT/'StudyFlowApp-login-fix').rglob('*'):
    if src.is_file():
        rel=src.relative_to(ROOT/'StudyFlowApp-login-fix');dest=PROJECT/rel
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==before[str(rel)],str(rel)
        shutil.copy2(src,dest)
print('Installed three-file correction.')
