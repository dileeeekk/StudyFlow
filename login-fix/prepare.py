from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
paths=['app/src/main/res/layout/activity_login.xml','app/src/main/res/values/login_strings.xml','app/src/main/java/com/example/studyflowapp/LoginActivity.kt']
baseline={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PROJECT/'app/src/main').rglob('*') if p.is_file()}
(ROOT/'before.json').write_text(json.dumps(baseline,indent=2))
for rel in paths:
    content=(PROJECT/rel).read_text(encoding='utf-8')
    backup=ROOT/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_text(content,encoding='utf-8')
    if rel.endswith('activity_login.xml'):
        content=content.replace(' android:hint="@string/login_email_hint"','').replace(' android:hint="@string/login_password_hint"','')
    elif rel.endswith('login_strings.xml'):
        content=re.sub(r'    <string name="login_(email|password)_hint">.*?</string>\n','',content)
    else:
        content=content.replace('import android.os.Bundle','import android.os.Build\nimport android.os.Bundle')
        content=content.replace('''        for (field in listOf(email, password)) {
''','''        for (field in listOf(email, password)) {
            // Keep taps and stylus input on the standard keyboard, including email.
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                field.setAutoHandwritingEnabled(false)
            }
            field.setOnClickListener {
                field.requestFocus()
                WindowInsetsControllerCompat(window, field).show(WindowInsetsCompat.Type.ime())
            }
''')
    dest=ROOT/'StudyFlowApp-login-fix'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(content,encoding='utf-8')
print('Prepared three-file correction and backups.')
