from pathlib import Path
import xml.etree.ElementTree as ET
import hashlib, json

HERE=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
OUT=HERE/'StudyFlowApp-login'
MAIN=OUT/'app/src/main'
def write(name,text):
    p=MAIN/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def xml(name,text): write('res/'+name,'<?xml version="1.0" encoding="utf-8"?>\n'+text)
ns='http://www.w3.org/2000/svg'
paths=list(ET.parse(r'C:\Users\admin\Downloads\Login.svg').getroot().iter('{'+ns+'}path'))
brand=ET.parse(r'C:\Users\admin\Downloads\Brand mark.svg').find('{'+ns+'}path').get('d')
def vector(name,path,size,color='studyflow_muted',x=0,y=0):
    xml('drawable/'+name+'.xml',f'''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="{size}dp" android:height="{size}dp" android:viewportWidth="{size}" android:viewportHeight="{size}">
    <group android:translateX="{x}" android:translateY="{y}">
        <path android:pathData="{path}" android:fillColor="@android:color/transparent" android:strokeColor="@color/{color}" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>''')
vector('ic_login_brand',brand,56,'studyflow_primary')
vector('ic_login_email',paths[4].get('d'),19,x=-313,y=-423.5)
vector('ic_login_eye_off',paths[5].get('d'),19,x=-313,y=-518.5)
vector('ic_login_eye','M1.632,9.224 C3.0,5.9 6.1,4 9.5,4 C12.9,4 16,5.9 17.368,9.224 Q17.467,9.5 17.368,9.775 C16,13.1 12.9,15 9.5,15 C6.1,15 3,13.1 1.632,9.775 Q1.533,9.5 1.632,9.224 M11.875,9.5 A2.375,2.375 0,1 1,7.125,9.5 A2.375,2.375 0,1 1,11.875,9.5',19)
check=paths[6].get('d')
vector('ic_login_checked',check,18,'studyflow_primary',-44,-574)
vector('ic_login_unchecked',check[check.index('M47.75'):],18,'studyflow_primary',-44,-574)
xml('drawable/login_checkbox.xml','''<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_checked="true" android:drawable="@drawable/ic_login_checked" />
    <item android:drawable="@drawable/ic_login_unchecked" />
</selector>''')
xml('drawable/bg_login_brand.xml','''<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <corners android:radius="18dp" />
    <gradient android:angle="270" android:startColor="#EDF2FF" android:centerColor="#F5F6FD" android:centerY="0.6" android:endColor="#EAE3FA" />
</shape>''')
xml('drawable/bg_login_card.xml','''<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/studyflow_white" />
    <corners android:radius="22dp" />
    <stroke android:width="1dp" android:color="@color/studyflow_outline" />
</shape>''')
xml('drawable/bg_login_field.xml','''<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_focused="true"><shape><solid android:color="@color/studyflow_white" /><corners android:radius="14dp" /><stroke android:width="1dp" android:color="@color/studyflow_primary" /></shape></item>
    <item><shape><solid android:color="@color/studyflow_white" /><corners android:radius="14dp" /><stroke android:width="1dp" android:color="@color/studyflow_outline" /></shape></item>
</selector>''')
xml('values/login_strings.xml',r'''<resources>
    <string name="login_brand">STUDYFLOW</string>
    <string name="login_title">Welcome back.\nFind your flow.</string>
    <string name="login_description">Your classes, goals and ideas.\nAll right where you left them.</string>
    <string name="login_email_label">Email address</string>
    <string name="login_email_hint">aruzhan.s@nu.edu.kz</string>
    <string name="login_password_label">Password</string>
    <string name="login_password_hint">••••••••••••</string>
    <string name="login_remember">Remember me</string>
    <string name="login_forgot">Forgot password?</string>
    <string name="login_submit">Log In</string>
    <string name="login_account_prompt">"New to StudyFlow? "</string>
    <string name="login_create_account">Create an account</string>
    <string name="login_legal">By continuing, you agree to our Terms of Service\nand Privacy Policy.</string>
    <string name="login_show_password">Show password</string>
    <string name="login_hide_password">Hide password</string>
</resources>''')
xml('values/login_styles.xml','''<resources>
    <style name="Theme.StudyFlowApp.Login" parent="Theme.StudyFlowApp.Onboarding" />
    <style name="StudyFlow.Login.Text" parent="StudyFlow.Onboarding.Text" />
    <style name="StudyFlow.Login.Label" parent="StudyFlow.Login.Text">
        <item name="android:fontFamily">@font/inter_semibold</item>
        <item name="android:textSize">12sp</item>
        <item name="android:minHeight">15dp</item>
    </style>
    <style name="StudyFlow.Login.Input" parent="Widget.AppCompat.EditText">
        <item name="android:background">@null</item>
        <item name="android:fontFamily">@font/inter_regular</item>
        <item name="android:includeFontPadding">false</item>
        <item name="android:letterSpacing">0</item>
        <item name="android:textSize">14sp</item>
        <item name="android:textColor">@color/studyflow_ink</item>
        <item name="android:textColorHint">@color/studyflow_ink</item>
        <item name="android:paddingStart">14dp</item>
        <item name="android:paddingEnd">48dp</item>
        <item name="android:paddingTop">0dp</item>
        <item name="android:paddingBottom">0dp</item>
        <item name="android:minHeight">0dp</item>
        <item name="android:gravity">center_vertical</item>
        <item name="android:singleLine">true</item>
    </style>
</resources>''')

# Reuse the existing button styling without changing previous pages.
existing=(PROJECT/'app/src/main/res/layout/activity_onboarding_focus.xml').read_text(encoding='utf-8')
button=existing[existing.index('        <FrameLayout\n            android:id="@+id/onboarding_button_container"'):existing.index('        <LinearLayout\n            android:id="@+id/onboarding_account_row"')]
button=button.replace('onboarding_button_container','login_button_container').replace('onboarding_get_started','login_submit').replace('onboarding_button_shadow','login_button_shadow').replace('android:layout_width="0dp"','android:layout_width="match_parent"').replace('android:layout_marginTop="22dp"','android:layout_marginTop="5dp"')
import re
button=re.sub(r'\s+app:layout_constraint\w+="[^"]+"','',button)

xml('layout/activity_login.xml','''<androidx.core.widget.NestedScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/login_scroll" android:layout_width="match_parent" android:layout_height="match_parent"
    android:fillViewport="true" android:clipToPadding="false" android:scrollbars="none"
    android:paddingTop="86dp" android:paddingBottom="34dp" android:focusableInTouchMode="true" android:descendantFocusability="beforeDescendants">
    <LinearLayout android:id="@+id/login_content" android:layout_width="match_parent" android:layout_height="wrap_content"
        android:orientation="vertical" android:paddingStart="4dp" android:paddingEnd="4dp"
        android:clipChildren="false" android:clipToPadding="false">
        <ImageView android:layout_width="56dp" android:layout_height="56dp" android:layout_marginStart="20dp"
            android:background="@drawable/bg_login_brand" android:src="@drawable/ic_login_brand" android:contentDescription="@null" android:importantForAccessibility="no" />
        <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text"
            android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="16dp"
            android:layout_marginHorizontal="20dp" android:layout_marginTop="18dp" android:fontFamily="@font/inter_bold"
            android:text="@string/login_brand" android:textSize="13sp" android:textColor="@color/studyflow_primary" />
        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/login_title" style="@style/StudyFlow.Login.Text"
            android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginHorizontal="20dp"
            android:layout_marginTop="17dp" android:fontFamily="@font/inter_bold" android:text="@string/login_title" android:textSize="34sp" app:lineHeight="39sp" />
        <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text"
            android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginHorizontal="20dp"
            android:layout_marginTop="17dp" android:paddingTop="2dp" android:paddingBottom="2dp" android:lineSpacingExtra="4sp"
            android:text="@string/login_description" android:textSize="14sp" android:textColor="@color/studyflow_muted" />
        <FrameLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="17dp"
            android:layout_marginBottom="-7dp" android:background="@drawable/login_card_shadow" android:clipChildren="false" android:clipToPadding="false">
            <LinearLayout android:id="@+id/login_card" android:layout_width="match_parent" android:layout_height="wrap_content"
                android:layout_marginHorizontal="20dp" android:layout_marginTop="15dp" android:layout_marginBottom="25dp"
                android:orientation="vertical" android:padding="20dp" android:background="@drawable/bg_login_card" android:clipChildren="false" android:clipToPadding="false">
                <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/login_email_label" android:labelFor="@id/login_email" />
                <FrameLayout android:layout_width="match_parent" android:layout_height="52dp" android:layout_marginTop="8dp" android:background="@drawable/bg_login_field" android:addStatesFromChildren="true">
                    <androidx.appcompat.widget.AppCompatEditText android:id="@+id/login_email" style="@style/StudyFlow.Login.Input"
                        android:layout_width="match_parent" android:layout_height="match_parent" android:hint="@string/login_email_hint"
                        android:inputType="textEmailAddress" android:imeOptions="actionNext" android:autofillHints="emailAddress" android:nextFocusForward="@id/login_password" />
                    <ImageView android:layout_width="19dp" android:layout_height="19dp" android:layout_gravity="end|center_vertical" android:layout_marginEnd="14dp" android:src="@drawable/ic_login_email" android:contentDescription="@null" android:importantForAccessibility="no" />
                </FrameLayout>
                <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="20dp" android:text="@string/login_password_label" android:labelFor="@id/login_password" />
                <FrameLayout android:layout_width="match_parent" android:layout_height="52dp" android:layout_marginTop="8dp" android:background="@drawable/bg_login_field" android:addStatesFromChildren="true">
                    <androidx.appcompat.widget.AppCompatEditText android:id="@+id/login_password" style="@style/StudyFlow.Login.Input"
                        android:layout_width="match_parent" android:layout_height="match_parent" android:hint="@string/login_password_hint"
                        android:inputType="textPassword" android:imeOptions="actionDone" android:autofillHints="password" android:saveEnabled="false" />
                    <androidx.appcompat.widget.AppCompatImageButton android:id="@+id/login_password_toggle" android:layout_width="48dp" android:layout_height="match_parent" android:layout_gravity="end"
                        android:background="?attr/selectableItemBackgroundBorderless" android:padding="0dp" android:scaleType="center" android:src="@drawable/ic_login_eye_off" android:contentDescription="@string/login_show_password" />
                </FrameLayout>
                <LinearLayout android:layout_width="match_parent" android:layout_height="48dp" android:layout_marginTop="5dp" android:orientation="horizontal" android:gravity="center_vertical">
                    <androidx.appcompat.widget.AppCompatCheckBox android:id="@+id/login_remember" style="@style/StudyFlow.Login.Text" android:layout_width="wrap_content" android:layout_height="match_parent"
                        android:button="@null" app:buttonCompat="@null" android:drawableStart="@drawable/login_checkbox" android:drawablePadding="7dp" android:padding="0dp" android:checked="true"
                        android:background="?attr/selectableItemBackgroundBorderless" android:gravity="center_vertical" android:text="@string/login_remember" android:textSize="11sp" android:textColor="@color/studyflow_muted" />
                    <Space android:layout_width="0dp" android:layout_height="1dp" android:layout_weight="1" />
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/login_forgot" style="@style/StudyFlow.Login.Text" android:layout_width="wrap_content" android:layout_height="match_parent"
                        android:gravity="center_vertical" android:fontFamily="@font/inter_semibold" android:text="@string/login_forgot" android:textSize="11sp" android:textColor="@color/studyflow_primary"
                        android:background="?attr/selectableItemBackgroundBorderless" android:clickable="true" android:focusable="true" />
                </LinearLayout>
'''+button+'''
            </LinearLayout>
        </FrameLayout>
        <LinearLayout android:layout_width="match_parent" android:layout_height="48dp" android:gravity="center" android:orientation="horizontal" android:layout_marginHorizontal="20dp">
            <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text" android:layout_width="wrap_content" android:layout_height="match_parent" android:gravity="center_vertical" android:text="@string/login_account_prompt" android:textSize="13sp" />
            <androidx.appcompat.widget.AppCompatTextView android:id="@+id/login_create_account" style="@style/StudyFlow.Login.Text" android:layout_width="wrap_content" android:layout_height="match_parent" android:gravity="center_vertical"
                android:fontFamily="@font/inter_semibold" android:text="@string/login_create_account" android:textSize="13sp" android:textColor="@color/studyflow_primary" android:background="?attr/selectableItemBackgroundBorderless" android:clickable="true" android:focusable="true" />
        </LinearLayout>
        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/login_legal" style="@style/StudyFlow.Login.Text" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginHorizontal="20dp"
            android:layout_marginTop="6dp" android:paddingTop="2dp" android:paddingBottom="2dp" android:gravity="center" android:text="@string/login_legal" android:textSize="11sp" app:lineHeight="17sp" android:textColor="@color/studyflow_muted" />
    </LinearLayout>
</androidx.core.widget.NestedScrollView>''')
# Horizontal margin is an API26 attribute; expand to compatible start/end.
layout=MAIN/'res/layout/activity_login.xml'
layout.write_text(layout.read_text(encoding='utf-8').replace('android:layout_marginHorizontal="20dp"','android:layout_marginStart="20dp" android:layout_marginEnd="20dp"'),encoding='utf-8')
write('java/com/example/studyflowapp/LoginActivity.kt','''package com.example.studyflowapp

import android.graphics.Color
import android.graphics.Rect
import android.os.Bundle
import android.text.method.HideReturnsTransformationMethod
import android.text.method.PasswordTransformationMethod
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.EditText
import android.widget.ImageButton
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.core.view.updatePadding

class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.rgb(23, 36, 67))
        )
        setContentView(R.layout.activity_login)
        val scroll = findViewById<View>(R.id.login_scroll)
        scroll.requestFocus()
        var previousImeBottom = 0
        ViewCompat.setOnApplyWindowInsetsListener(scroll) { view, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            val cutout = insets.getInsets(WindowInsetsCompat.Type.displayCutout())
            val ime = insets.getInsets(WindowInsetsCompat.Type.ime())
            view.updatePadding(
                left = maxOf(bars.left, cutout.left),
                top = maxOf(bars.top, cutout.top, dp(44)) + dp(42),
                right = maxOf(bars.right, cutout.right),
                bottom = maxOf(bars.bottom, cutout.bottom, ime.bottom, dp(34))
            )
            if (ime.bottom > previousImeBottom) {
                currentFocus?.takeIf { it is EditText }?.let { field ->
                    field.post { field.requestRectangleOnScreen(Rect(0, 0, field.width, field.height), false) }
                }
            }
            previousImeBottom = ime.bottom
            insets
        }
        ViewCompat.requestApplyInsets(scroll)

        val password = findViewById<EditText>(R.id.login_password)
        val toggle = findViewById<ImageButton>(R.id.login_password_toggle)
        toggle.setOnClickListener {
            val start = password.selectionStart
            val end = password.selectionEnd
            val show = password.transformationMethod is PasswordTransformationMethod
            password.transformationMethod = if (show) HideReturnsTransformationMethod.getInstance()
                else PasswordTransformationMethod.getInstance()
            if (start >= 0 && end >= 0) password.setSelection(start, end)
            toggle.setImageResource(if (show) R.drawable.ic_login_eye else R.drawable.ic_login_eye_off)
            toggle.setContentDescription(getString(if (show) R.string.login_hide_password else R.string.login_show_password))
        }
        fun closeKeyboard() {
            WindowInsetsControllerCompat(window, scroll).hide(WindowInsetsCompat.Type.ime())
            scroll.requestFocus()
        }
        // UI preview only: no credential validation, storage or network requests.
        findViewById<View>(R.id.login_submit).setOnClickListener { closeKeyboard() }
        password.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) { closeKeyboard(); true } else false
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
''')
activity=(PROJECT/'app/src/main/java/com/example/studyflowapp/OnboardingActivity.kt').read_text(encoding='utf-8')
activity=activity.replace('// Skip, Log In and the final page CTA use ripple feedback only.','''else {
            findViewById<View>(R.id.onboarding_get_started).setOnClickListener { openLogin() }
        }
        login.setOnClickListener { openLogin() }
        findViewById<View>(R.id.onboarding_skip).setOnClickListener { openLogin() }''')
activity=activity.replace('    override fun onResume()', '''    private fun openLogin() {
        if (!openingNextPage) {
            openingNextPage = true
            startActivity(Intent(this, LoginActivity::class.java))
        }
    }

    override fun onResume()''')
write('java/com/example/studyflowapp/OnboardingActivity.kt',activity)
manifest=(PROJECT/'app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
manifest=manifest.replace('    </application>','''        <activity
            android:name=".LoginActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Login"
            android:windowSoftInputMode="adjustResize|stateAlwaysHidden" />
    </application>''')
write('AndroidManifest.xml',manifest)
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline={str(p.relative_to(PROJECT)):digest(p) for p in (PROJECT/'app/src/main').rglob('*') if p.is_file()}
(HERE/'before.json').write_text(json.dumps(baseline,indent=2),encoding='utf-8')
for p in MAIN.rglob('*.xml'): ET.parse(p)
print('Login sources prepared; original project hashes captured.')
