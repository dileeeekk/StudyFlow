from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
OUT=ROOT/'StudyFlowApp-register-validation'
(ROOT/'before.json').write_text(json.dumps({str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PROJECT/'app/src/main').rglob('*') if p.is_file()},indent=2))
def write(rel,text):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
rel='app/src/main/res/layout/activity_register.xml';t=(PROJECT/rel).read_text(encoding='utf-8')
t=t.replace('android:layout_marginTop="7dp" android:text="@string/register_password_helper"','android:id="@+id/register_password_error" android:visibility="invisible" android:accessibilityLiveRegion="polite"\n                    android:layout_marginTop="7dp" android:text="@string/register_password_helper"').replace('android:textColor="@color/studyflow_register_helper"','android:textColor="@color/studyflow_register_error"')
write(rel,t)
rel='app/src/main/res/values/register_colors.xml';t=(PROJECT/rel).read_text(encoding='utf-8').replace('<color name="studyflow_register_helper">#23816B</color>','<color name="studyflow_register_error">#D32F2F</color>');write(rel,t)
rel='app/src/main/java/com/example/studyflowapp/RegisterActivity.kt';t=(PROJECT/rel).read_text(encoding='utf-8')
t=t.replace('import android.widget.EditText','import android.widget.CheckBox\nimport androidx.core.widget.doAfterTextChanged\nimport android.widget.EditText')
t=t.replace('        val email = findViewById<EditText>(R.id.register_email)', '''        val passwordError = findViewById<View>(R.id.register_password_error)
        fun updatePasswordError() {
            val length = Character.codePointCount(password.text, 0, password.text.length)
            passwordError.visibility = if (length in 1..7) View.VISIBLE else View.INVISIBLE
        }
        password.doAfterTextChanged { updatePasswordError() }
        updatePasswordError()

        val agreement = findViewById<CheckBox>(R.id.register_agreement)
        val submit = findViewById<View>(R.id.register_submit)
        val buttonContainer = findViewById<View>(R.id.register_button_container)
        fun updateAgreementState() {
            submit.isEnabled = agreement.isChecked
            buttonContainer.alpha = if (agreement.isChecked) 1f else 0.45f
        }
        agreement.setOnCheckedChangeListener { _, _ -> updateAgreementState() }
        updateAgreementState()

        val email = findViewById<EditText>(R.id.register_email)''')
t=t.replace('// UI preview only: no credential validation, storage or network requests.','// UI feedback only: no account creation, storage or network requests.')
t=t.replace('findViewById<View>(R.id.register_submit).setOnClickListener { closeKeyboard() }','submit.setOnClickListener { if (agreement.isChecked) closeKeyboard() }')
write(rel,t)
print('Prepared consent button state and inline password error.')
