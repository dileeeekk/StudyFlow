from pathlib import Path
import shutil
root=Path(__file__).resolve().parent
p=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
for f in (root/'files').rglob('*'):
 if not f.is_file():continue
 rel=f.relative_to(root/'files');target=p/rel;backup=root/'backup'/rel
 if target.exists() and not backup.exists():backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,backup)
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
 # Keep the existing handoff copy consistent, scoped to the same changed files.
 mirror=root.parent/'android'/rel;mirror.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,mirror)
print('Installed planner files; original files backed up.')
