from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
OUT=ROOT/'StudyFlowApp-register-update'
baseline={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PROJECT/'app/src/main').rglob('*') if p.is_file()}
(ROOT/'before.json').write_text(json.dumps(baseline,indent=2))
def write(rel,t):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
rel='app/src/main/res/layout/activity_register.xml';t=(PROJECT/rel).read_text(encoding='utf-8')
start=t.index('<androidx.appcompat.widget.AppCompatTextView android:id="@+id/register_university"')
end=t.index('            </LinearLayout>\n        </FrameLayout>',start)
t=t[:start]+'''<androidx.appcompat.widget.AppCompatEditText
                    android:id="@+id/register_university"
                    style="@style/StudyFlow.Login.Input"
                    android:layout_width="match_parent"
                    android:layout_height="52dp"
                    android:layout_marginTop="8dp"
                    android:background="@drawable/bg_login_field"
                    android:backgroundTint="@null"
                    android:paddingEnd="14dp"
                    android:inputType="textCapWords"
                    android:imeOptions="actionDone" />
'''+t[end:]
t=t.replace('android:imeOptions="actionDone" android:autofillHints="newPassword"','android:imeOptions="actionNext" android:nextFocusForward="@id/register_university" android:autofillHints="newPassword"')
write(rel,t)
rel='app/src/main/java/com/example/studyflowapp/RegisterActivity.kt';t=(PROJECT/rel).read_text(encoding='utf-8')
t=t.replace('        for (field in listOf(findViewById<EditText>(R.id.register_name), email, password)) {','        val university = findViewById<EditText>(R.id.register_university)\n        for (field in listOf(findViewById<EditText>(R.id.register_name), email, password, university)) {')
t=t.replace('password.setOnEditorActionListener','university.setOnEditorActionListener')
write(rel,t)
rel='app/src/main/res/values/register_strings.xml';t=(PROJECT/rel).read_text(encoding='utf-8');t=re.sub(r'    <string name="register_(year|group)_label">.*?</string>\n','',t);write(rel,t)
(OUT/'app/src/main/res/drawable-xxhdpi').mkdir(parents=True,exist_ok=True)
print('Prepared editable University and removed Year/Group row.')
