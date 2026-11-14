from pathlib import Path
import shutil
root=Path(__file__).resolve().parent
p=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp\gradle.properties')
backup=root/'gradle.properties.before-cloud'
if not backup.exists(): shutil.copy2(p,backup)
text=p.read_text(encoding='utf-8')
lines=[line for line in text.splitlines() if not line.startswith(('STUDYFLOW_API_URL=','STUDYFLOW_RELEASE_API_URL=','# Local Django over USB'))]
lines+=['# StudyFlow public HTTPS backend.', 'STUDYFLOW_API_URL=https://dileeeekk.pythonanywhere.com/api/', 'STUDYFLOW_RELEASE_API_URL=https://dileeeekk.pythonanywhere.com/api/']
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Android API configured for public HTTPS.')
