from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
OUT=ROOT/'android'
before={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PROJECT/'app').rglob('*') if p.is_file() and 'build' not in p.relative_to(PROJECT).parts}
if (ROOT/'before.json').exists():
    assert json.loads((ROOT/'before.json').read_text()) == before, 'Project changed since preparation'
else:
    (ROOT/'before.json').write_text(json.dumps(before,indent=2))
def read(rel):return (PROJECT/rel).read_text(encoding='utf-8')
def write(rel,text):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')

rel='app/build.gradle.kts';t=read(rel)
t=t.replace('    buildTypes {','''    buildFeatures { buildConfig = true }
    buildTypes {''')
t=t.replace('        release {','''        debug {
            val api = providers.gradleProperty("STUDYFLOW_API_URL").orElse("http://10.0.2.2:8000/api/").get()
            buildConfigField("String", "API_BASE_URL", "\\\"${api.replace("\\\\", "\\\\\\\\").replace("\\\"", "\\\\\\\"")}\\\"")
        }
        release {
            val api = providers.gradleProperty("STUDYFLOW_RELEASE_API_URL").orElse("").get()
            buildConfigField("String", "API_BASE_URL", "\\\"${api.replace("\\\\", "\\\\\\\\").replace("\\\"", "\\\\\\\"")}\\\"")''')
t=t.replace('dependencies {','''dependencies {
    implementation("androidx.lifecycle:lifecycle-viewmodel:2.11.0")
    implementation("androidx.lifecycle:lifecycle-livedata-core:2.11.0")''')
write(rel,t)
rel='app/src/main/AndroidManifest.xml';t=read(rel).replace('    <application','    <uses-permission android:name="android.permission.INTERNET" />\n\n    <application',1).replace('android:allowBackup="true"','android:allowBackup="true"\n        android:usesCleartextTraffic="false"')
write(rel,t)

for activity,prefix in [('Login','login'),('Register','register')]:
    rel=f'app/src/main/java/com/example/studyflowapp/{activity}Activity.kt';t=read(rel)
    t=t.replace('import androidx.appcompat.app.AppCompatActivity','''import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.auth.AuthViewModel
import com.example.studyflowapp.auth.NetworkActivity
import com.google.android.material.button.MaterialButton
import com.google.android.material.dialog.MaterialAlertDialogBuilder''')
    t=t.replace(f'class {activity}Activity : AppCompatActivity()',f'class {activity}Activity : NetworkActivity()')
    t=t.replace('    private var openingHome = false','    private var openingHome = false\n    private var authBusy = false')
    t=t.replace(f'        setContentView(R.layout.activity_{prefix})',f'        setContentView(R.layout.activity_{prefix})\n        val auth = ViewModelProvider(this)[AuthViewModel::class.java]')
    t=t.replace('val enabled = formIsValid()','val enabled = formIsValid() && !authBusy')
    start=t.index('        // Local form feedback only' if activity=='Login' else '        // UI feedback only:')
    end=t.index('        password.setOnEditorActionListener' if activity=='Login' else '        university.setOnEditorActionListener',start)
    invoke='auth.login(email.text.toString(), password.text.toString())' if activity=='Login' else 'auth.register(name.text.toString(), email.text.toString(), password.text.toString(), university.text.toString(), agreement.isChecked)'
    fields='listOf(email, password)' if activity=='Login' else 'fields'
    extras='findViewById<View>(R.id.login_create_account).isEnabled = !state.loading' if activity=='Login' else 'agreement.isEnabled = !state.loading\n            findViewById<View>(R.id.register_login).isEnabled = !state.loading'
    loading='auth_signing_in' if activity=='Login' else 'auth_registering'
    t=t[:start]+f'''        // Credentials are sent only to Django; Home opens only after a successful response.
        submit.setOnClickListener {{
            if (formIsValid() && !authBusy && !openingHome) {{
                withNetworkAccess {{
                    closeKeyboard()
                    {invoke}
                }}
            }}
        }}
        auth.state.observe(this) {{ state ->
            authBusy = state.loading
            for (field in {fields}) field.isEnabled = !state.loading
            toggle.isEnabled = !state.loading
            {extras}
            (submit as MaterialButton).setText(if (state.loading) R.string.{loading} else R.string.{prefix}_submit)
            updateFormState()
            if (state.user != null && !openingHome) {{
                openingHome = true
                password.text.clear()
                auth.consumeResult()
                startActivity(Intent(this, HomeActivity::class.java)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
                finish()
            }} else if (state.error != null) {{
                val message = state.error
                auth.consumeResult()
                MaterialAlertDialogBuilder(this).setTitle(R.string.auth_error_title)
                    .setMessage(message).setPositiveButton(android.R.string.ok, null).show()
            }}
        }}
'''+t[end:]
    write(rel,t)

rel='app/src/main/java/com/example/studyflowapp/HomeActivity.kt';t=read(rel)
t=t.replace('import android.graphics.Color','import android.content.Intent\nimport android.widget.TextView\nimport android.widget.Toast\nimport android.graphics.Color')
t=t.replace('import androidx.appcompat.app.AppCompatActivity','''import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.auth.AuthViewModel
import com.example.studyflowapp.auth.NetworkActivity
import com.google.android.material.dialog.MaterialAlertDialogBuilder''')
t=t.replace('/** Figma preview data only. Tasks, notifications and other tabs are not connected yet. */','/** Authenticated account; task and schedule cards still contain Figma preview data. */')
t=t.replace('class HomeActivity : AppCompatActivity()', 'class HomeActivity : NetworkActivity()')
point='        val root = findViewById<View>(R.id.home_root)'
t=t.replace(point,point+'''
        val auth = ViewModelProvider(this)[AuthViewModel::class.java]
        root.visibility = View.INVISIBLE
        fun returnToLogin() {
            startActivity(Intent(this, LoginActivity::class.java)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
            finish()
        }
        auth.state.observe(this) { state ->
            if (state.expired || state.loggedOut) {
                state.error?.let { Toast.makeText(this, it, Toast.LENGTH_LONG).show() }
                returnToLogin()
            } else if (state.user != null) {
                root.visibility = View.VISIBLE
                val user = state.user
                val firstName = user.fullName.trim().split(Regex("\\\\s+"), limit = 2).first()
                findViewById<TextView>(R.id.home_greeting).text = getString(R.string.auth_greeting, firstName)
                findViewById<View>(R.id.home_tab_profile).setOnClickListener {
                    if (auth.state.value?.loading == true) return@setOnClickListener
                    MaterialAlertDialogBuilder(this).setTitle(R.string.auth_account)
                        .setMessage("${user.fullName}\\n${user.email}\\n${user.university}")
                        .setNegativeButton(R.string.auth_cancel, null)
                        .setPositiveButton(R.string.auth_logout) { _, _ -> auth.logout() }.show()
                }
            } else if (state.error != null) {
                MaterialAlertDialogBuilder(this).setTitle(R.string.auth_offline_title)
                    .setMessage(state.error).setCancelable(false)
                    .setPositiveButton(R.string.auth_retry) { _, _ -> withNetworkAccess { auth.loadProfile(retry = true) } }
                    .setNegativeButton(R.string.auth_logout) { _, _ -> auth.logout() }.show()
            }
        }
        withNetworkAccess { auth.loadProfile() }
''')
write(rel,t)
rel='app/src/main/java/com/example/studyflowapp/MainActivity.kt';t=read(rel)
t=t.replace('import android.content.Intent','import com.example.studyflowapp.auth.AuthRepository\nimport android.content.Intent')
t=t.replace('            startActivity(Intent(this, OnboardingActivity::class.java))','''            val signedIn = runCatching { AuthRepository.get(this).hasSession() }.getOrDefault(false)
            val destination = if (signedIn) HomeActivity::class.java else OnboardingActivity::class.java
            startActivity(Intent(this, destination))''')
write(rel,t)
print('Prepared Android integration; XML layouts unchanged.')
