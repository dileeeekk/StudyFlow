from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
OUT=ROOT/'StudyFlowApp-auth-validation'
(ROOT/'before.json').write_text(json.dumps({str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PROJECT/'app/src/main').rglob('*') if p.is_file()},indent=2))
def write(rel,text):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
rel='app/src/main/res/layout/activity_login.xml';t=(PROJECT/rel).read_text(encoding='utf-8')
a=t.index('                    <androidx.appcompat.widget.AppCompatCheckBox android:id="@+id/login_remember"');b=t.index('                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/login_forgot"',a)
t=t[:a]+'''                    <androidx.appcompat.widget.AppCompatTextView
                        android:id="@+id/login_password_error"
                        style="@style/StudyFlow.Login.Text"
                        android:layout_width="0dp"
                        android:layout_height="match_parent"
                        android:layout_weight="1"
                        android:paddingTop="2dp"
                        android:paddingEnd="8dp"
                        android:gravity="top"
                        android:visibility="invisible"
                        android:accessibilityLiveRegion="polite"
                        android:text="@string/register_password_helper"
                        android:textSize="10sp"
                        android:textColor="@color/studyflow_register_error" />
'''+t[b:];write(rel,t)
rel='app/src/main/res/values/login_strings.xml';t=(PROJECT/rel).read_text(encoding='utf-8');t=re.sub(r'    <string name="login_remember">.*?</string>\n','',t);write(rel,t)
rel='app/src/main/java/com/example/studyflowapp/LoginActivity.kt';t=(PROJECT/rel).read_text(encoding='utf-8')
t=t.replace('import android.view.View\n','import android.view.View\nimport android.view.ViewGroup\nimport androidx.core.widget.doAfterTextChanged\n')
t=t.replace('        for (field in listOf(email, password)) {','''        val passwordError = findViewById<View>(R.id.login_password_error)
        val submit = findViewById<View>(R.id.login_submit)
        val buttonContainer = findViewById<ViewGroup>(R.id.login_button_container)
        fun formIsValid(): Boolean = email.text.isNotBlank() && password.text.isNotBlank() &&
            Character.codePointCount(password.text, 0, password.text.length) >= 8
        fun updateFormState() {
            val length = Character.codePointCount(password.text, 0, password.text.length)
            passwordError.visibility = if (length in 1..7) View.VISIBLE else View.INVISIBLE
            val enabled = formIsValid()
            submit.isEnabled = enabled
            for (index in 0 until buttonContainer.childCount) {
                buttonContainer.getChildAt(index).alpha = if (enabled) 1f else 0.45f
            }
        }
        for (field in listOf(email, password)) {
            field.doAfterTextChanged { updateFormState() }''')
t=t.replace('        val toggle =','        updateFormState()\n        val toggle =')
t=t.replace('// UI preview only: no credential validation, storage or network requests.','// Local form feedback only; account verification is not connected.')
t=t.replace('findViewById<View>(R.id.login_submit).setOnClickListener { closeKeyboard() }','submit.setOnClickListener { if (formIsValid()) closeKeyboard() }')
write(rel,t)
rel='app/src/main/java/com/example/studyflowapp/RegisterActivity.kt';t=(PROJECT/rel).read_text(encoding='utf-8').replace('import android.view.View\n','import android.view.View\nimport android.view.ViewGroup\n')
a=t.index('        val password = findViewById<EditText>(R.id.register_password)');b=t.index('            field.setOnClickListener',a)
t=t[:a]+'''        val name = findViewById<EditText>(R.id.register_name)
        val email = findViewById<EditText>(R.id.register_email)
        val password = findViewById<EditText>(R.id.register_password)
        val university = findViewById<EditText>(R.id.register_university)
        val fields = listOf(name, email, password, university)
        val passwordError = findViewById<View>(R.id.register_password_error)
        val agreement = findViewById<CheckBox>(R.id.register_agreement)
        val submit = findViewById<View>(R.id.register_submit)
        val buttonContainer = findViewById<ViewGroup>(R.id.register_button_container)
        fun formIsValid(): Boolean = agreement.isChecked && fields.all { it.text.isNotBlank() } &&
            Character.codePointCount(password.text, 0, password.text.length) >= 8
        fun updateFormState() {
            val length = Character.codePointCount(password.text, 0, password.text.length)
            passwordError.visibility = if (length in 1..7) View.VISIBLE else View.INVISIBLE
            val enabled = formIsValid()
            submit.isEnabled = enabled
            for (index in 0 until buttonContainer.childCount) {
                buttonContainer.getChildAt(index).alpha = if (enabled) 1f else 0.45f
            }
        }
        agreement.setOnCheckedChangeListener { _, _ -> updateFormState() }
        for (field in fields) {
            field.doAfterTextChanged { updateFormState() }
'''+t[b:]
t=t.replace('        val toggle =','        updateFormState()\n        val toggle =').replace('submit.setOnClickListener { if (agreement.isChecked) closeKeyboard() }','submit.setOnClickListener { if (formIsValid()) closeKeyboard() }')
write(rel,t)
print('Prepared both form states and removed Remember me.')
