from pathlib import Path
import hashlib
import json
import shutil
import zipfile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
PROJECT = Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE = HERE / 'StudyFlowApp-onboarding'
MAIN = PACKAGE / 'app/src/main'

def write(name, content):
    p = MAIN / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip() + '\n', encoding='utf-8')

write('java/com/example/studyflowapp/MainActivity.kt', '''
package com.example.studyflowapp

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private val handler = Handler(Looper.getMainLooper())
    private val openOnboarding = Runnable {
        startActivity(Intent(this, OnboardingActivity::class.java))
        finish()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.dark(Color.TRANSPARENT)
        )
        setContentView(R.layout.activity_main)
    }

    override fun onStart() {
        super.onStart()
        // Temporary UI transition; no loading or account checks yet.
        handler.postDelayed(openOnboarding, 1_200L)
    }

    override fun onStop() {
        handler.removeCallbacks(openOnboarding)
        super.onStop()
    }
}
''')

write('java/com/example/studyflowapp/OnboardingActivity.kt', '''
package com.example.studyflowapp

import android.graphics.Color
import android.graphics.Rect
import android.os.Bundle
import android.view.TouchDelegate
import android.view.View
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updatePadding

class OnboardingActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(
                Color.TRANSPARENT,
                Color.rgb(23, 36, 67)
            )
        )
        setContentView(R.layout.activity_onboarding)

        // The View API works from API 21; the XML attribute requires API 31.
        findViewById<View>(R.id.onboarding_hero).clipToOutline = true

        val scroll = findViewById<View>(R.id.onboarding_scroll)
        ViewCompat.setOnApplyWindowInsetsListener(scroll) { view, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            val cutout = insets.getInsets(WindowInsetsCompat.Type.displayCutout())
            view.updatePadding(
                left = maxOf(bars.left, cutout.left),
                top = maxOf(bars.top, cutout.top, dp(44)) + dp(10),
                right = maxOf(bars.right, cutout.right),
                bottom = maxOf(bars.bottom, cutout.bottom, dp(34))
            )
            insets
        }
        ViewCompat.requestApplyInsets(scroll)

        // Make the small Log In text easier to tap without changing its position.
        val login = findViewById<View>(R.id.onboarding_login)
        val footer = findViewById<View>(R.id.onboarding_account_row)
        footer.post {
            val touchArea = Rect()
            login.getHitRect(touchArea)
            touchArea.inset(-dp(12), 0)
            footer.touchDelegate = TouchDelegate(touchArea, login)
        }
        // Buttons currently use their XML ripple feedback only.
    }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density + 0.5f).toInt()
}
''')

write('res/layout/activity_onboarding.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<androidx.core.widget.NestedScrollView
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/onboarding_scroll"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fillViewport="true"
    android:overScrollMode="never"
    android:paddingTop="54dp"
    android:paddingBottom="34dp"
    android:scrollbars="none"
    tools:background="@color/studyflow_white"
    tools:context=".OnboardingActivity">

    <androidx.constraintlayout.widget.ConstraintLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:clipChildren="false"
        android:clipToPadding="false"
        android:paddingStart="24dp"
        android:paddingEnd="24dp">

        <androidx.appcompat.widget.AppCompatTextView
            android:id="@+id/onboarding_brand"
            style="@style/StudyFlow.Onboarding.Text"
            android:layout_width="wrap_content"
            android:layout_height="48dp"
            android:fontFamily="@font/inter_bold"
            android:gravity="center_vertical"
            android:text="@string/studyflow_splash_title"
            android:textSize="16sp"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toTopOf="parent" />

        <androidx.appcompat.widget.AppCompatTextView
            android:id="@+id/onboarding_skip"
            style="@style/StudyFlow.Onboarding.Text"
            android:layout_width="wrap_content"
            android:layout_height="48dp"
            android:background="?attr/selectableItemBackgroundBorderless"
            android:clickable="true"
            android:focusable="true"
            android:fontFamily="@font/inter_medium"
            android:gravity="end|center_vertical"
            android:minWidth="48dp"
            android:text="@string/onboarding_skip"
            android:textColor="@color/studyflow_muted"
            android:textSize="13sp"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintTop_toTopOf="parent" />

        <androidx.constraintlayout.widget.ConstraintLayout
            android:id="@+id/onboarding_hero"
            android:layout_width="0dp"
            android:layout_height="0dp"
            android:layout_marginTop="14dp"
            android:background="@drawable/bg_onboarding_hero"
            android:importantForAccessibility="noHideDescendants"
            app:layout_constraintDimensionRatio="342:332"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@id/onboarding_brand">

            <ImageView
                android:id="@+id/onboarding_illustration"
                android:layout_width="0dp"
                android:layout_height="0dp"
                android:contentDescription="@null"
                android:scaleType="centerCrop"
                android:src="@drawable/onboarding_academic_illustration"
                app:layout_constraintDimensionRatio="342:280"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintStart_toStartOf="parent"
                app:layout_constraintTop_toTopOf="parent" />

            <LinearLayout
                android:layout_width="0dp"
                android:layout_height="60dp"
                android:layout_marginStart="14dp"
                android:layout_marginEnd="14dp"
                android:layout_marginBottom="24dp"
                android:background="@drawable/bg_onboarding_deadline"
                android:gravity="center_vertical"
                android:orientation="vertical"
                android:paddingStart="14dp"
                android:paddingEnd="14dp"
                app:layout_constraintBottom_toBottomOf="parent"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintStart_toStartOf="parent">

                <androidx.appcompat.widget.AppCompatTextView
                    style="@style/StudyFlow.Onboarding.Text"
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:fontFamily="@font/inter_semibold"
                    android:text="@string/onboarding_deadline_title"
                    android:textSize="12sp" />

                <androidx.appcompat.widget.AppCompatTextView
                    style="@style/StudyFlow.Onboarding.Text"
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:layout_marginTop="4dp"
                    android:text="@string/onboarding_deadline_detail"
                    android:textColor="@color/studyflow_muted"
                    android:textSize="10sp" />
            </LinearLayout>
        </androidx.constraintlayout.widget.ConstraintLayout>

        <androidx.appcompat.widget.AppCompatTextView
            android:id="@+id/onboarding_badge"
            style="@style/StudyFlow.Onboarding.Text"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="26dp"
            android:background="@drawable/bg_onboarding_badge"
            android:fontFamily="@font/inter_semibold"
            android:gravity="center_vertical"
            android:minHeight="22dp"
            android:minWidth="207dp"
            android:paddingStart="9dp"
            android:paddingEnd="9dp"
            android:text="@string/onboarding_badge"
            android:textColor="@color/studyflow_primary"
            android:textSize="10sp"
            app:layout_constrainedWidth="true"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintHorizontal_bias="0"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@id/onboarding_hero" />

        <androidx.appcompat.widget.AppCompatTextView
            android:id="@+id/onboarding_title"
            style="@style/StudyFlow.Onboarding.Text"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_marginTop="13dp"
            android:fontFamily="@font/inter_bold"
            android:text="@string/onboarding_title"
            android:textSize="32sp"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@id/onboarding_badge" />

        <androidx.appcompat.widget.AppCompatTextView
            android:id="@+id/onboarding_description"
            style="@style/StudyFlow.Onboarding.Text"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_marginTop="12dp"
            android:breakStrategy="simple"
            android:hyphenationFrequency="none"
            android:lineSpacingExtra="4sp"
            android:paddingTop="2dp"
            android:paddingBottom="2dp"
            android:text="@string/onboarding_description"
            android:textColor="@color/studyflow_muted"
            android:textSize="14sp"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@id/onboarding_title" />

        <LinearLayout
            android:id="@+id/onboarding_pagination"
            android:layout_width="wrap_content"
            android:layout_height="7dp"
            android:layout_marginTop="30dp"
            android:importantForAccessibility="noHideDescendants"
            android:orientation="horizontal"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@id/onboarding_description">

            <View
                android:layout_width="26dp"
                android:layout_height="7dp"
                android:background="@drawable/bg_onboarding_page_active" />
            <View
                android:layout_width="7dp"
                android:layout_height="7dp"
                android:layout_marginStart="6dp"
                android:background="@drawable/bg_onboarding_page_inactive" />
            <View
                android:layout_width="7dp"
                android:layout_height="7dp"
                android:layout_marginStart="6dp"
                android:background="@drawable/bg_onboarding_page_inactive" />
        </LinearLayout>

        <FrameLayout
            android:id="@+id/onboarding_button_container"
            android:layout_width="0dp"
            android:layout_height="52dp"
            android:layout_marginTop="22dp"
            android:clipChildren="false"
            android:clipToPadding="false"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@id/onboarding_pagination">

            <!-- The shadow extends beyond the 52dp button, as in the SVG. -->
            <ImageView
                android:layout_width="match_parent"
                android:layout_height="92dp"
                android:layout_gravity="center_vertical"
                android:layout_marginStart="-20dp"
                android:layout_marginEnd="-20dp"
                android:contentDescription="@null"
                android:importantForAccessibility="no"
                android:scaleType="fitXY"
                android:src="@drawable/onboarding_button_shadow"
                android:translationY="8dp" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/onboarding_get_started"
                android:layout_width="match_parent"
                android:layout_height="match_parent"
                android:elevation="0dp"
                android:fontFamily="@font/inter_semibold"
                android:gravity="center"
                android:includeFontPadding="false"
                android:insetTop="0dp"
                android:insetBottom="0dp"
                android:letterSpacing="0"
                android:minHeight="52dp"
                android:minWidth="0dp"
                android:paddingStart="16dp"
                android:paddingEnd="16dp"
                android:paddingTop="0dp"
                android:paddingBottom="0dp"
                android:stateListAnimator="@null"
                android:text="@string/onboarding_get_started"
                android:textAllCaps="false"
                android:textColor="@color/studyflow_white"
                android:textSize="14sp"
                app:backgroundTint="@color/studyflow_primary"
                app:cornerRadius="14dp"
                app:icon="@drawable/ic_onboarding_arrow"
                app:iconGravity="textStart"
                app:iconPadding="12dp"
                app:iconSize="16dp"
                app:iconTint="@color/studyflow_white"
                app:rippleColor="#33FFFFFF"
                app:strokeColor="@color/studyflow_primary"
                app:strokeWidth="1dp" />
        </FrameLayout>

        <LinearLayout
            android:id="@+id/onboarding_account_row"
            android:layout_width="wrap_content"
            android:layout_height="48dp"
            android:layout_marginTop="5.5dp"
            android:baselineAligned="true"
            android:gravity="center"
            android:orientation="horizontal"
            app:layout_constraintBottom_toBottomOf="parent"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@id/onboarding_button_container"
            app:layout_constraintVertical_bias="0">

            <androidx.appcompat.widget.AppCompatTextView
                style="@style/StudyFlow.Onboarding.Text"
                android:layout_width="wrap_content"
                android:layout_height="match_parent"
                android:gravity="center_vertical"
                android:text="@string/onboarding_account_prompt"
                android:textColor="@color/studyflow_muted"
                android:textSize="12sp" />

            <androidx.appcompat.widget.AppCompatTextView
                android:id="@+id/onboarding_login"
                style="@style/StudyFlow.Onboarding.Text"
                android:layout_width="wrap_content"
                android:layout_height="match_parent"
                android:background="?attr/selectableItemBackgroundBorderless"
                android:clickable="true"
                android:focusable="true"
                android:fontFamily="@font/inter_semibold"
                android:gravity="center_vertical"
                android:text="@string/onboarding_login"
                android:textColor="@color/studyflow_primary"
                android:textSize="12sp" />
        </LinearLayout>
    </androidx.constraintlayout.widget.ConstraintLayout>
</androidx.core.widget.NestedScrollView>
''')

write('res/values/onboarding_colors.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="studyflow_ink">#172443</color>
    <color name="studyflow_muted">#66728B</color>
    <color name="studyflow_primary">#4564ED</color>
    <color name="studyflow_outline">#E5EAF3</color>
    <color name="studyflow_badge_background">#EDF1FF</color>
</resources>
''')

write('res/values/onboarding_strings.xml', r'''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="onboarding_skip">Skip</string>
    <string name="onboarding_deadline_title">Your next deadline, handled</string>
    <string name="onboarding_deadline_detail">Calculus II · Problem set 04</string>
    <string name="onboarding_badge">01 / YOUR ACADEMIC LIFE, SIMPLIFIED</string>
    <string name="onboarding_title">Track Every Deadline</string>
    <string name="onboarding_description">Bring assignments, exams and projects together.\nKnow what’s next before it becomes urgent.</string>
    <string name="onboarding_get_started">Get Started</string>
    <string name="onboarding_account_prompt">"Already have an account? "</string>
    <string name="onboarding_login">Log In</string>
</resources>
''')

write('res/values/onboarding_styles.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.StudyFlowApp.Onboarding" parent="Theme.Material3.Light.NoActionBar">
        <item name="android:windowBackground">@color/studyflow_white</item>
        <item name="android:windowLightStatusBar">true</item>
        <item name="android:colorAccent">@color/studyflow_primary</item>
        <item name="colorPrimary">@color/studyflow_primary</item>
        <item name="colorOnPrimary">@color/studyflow_white</item>
    </style>

    <style name="StudyFlow.Onboarding.Text" parent="">
        <item name="android:fontFamily">@font/inter_regular</item>
        <item name="android:includeFontPadding">false</item>
        <item name="android:letterSpacing">0</item>
        <item name="android:textColor">@color/studyflow_ink</item>
    </style>
</resources>
''')

write('res/drawable/bg_onboarding_hero.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="30dp" />
    <gradient
        android:angle="270"
        android:startColor="#EDF2FF"
        android:centerColor="#F5F6FD"
        android:centerY="0.6"
        android:endColor="#EAE3FA"
        android:type="linear" />
</shape>
''')
write('res/drawable/bg_onboarding_deadline.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="18dp" />
    <solid android:color="#D9FFFFFF" />
    <stroke android:width="1dp" android:color="@color/studyflow_white" />
</shape>
''')

for file, color, radius in [
    ('bg_onboarding_badge', 'studyflow_badge_background', 11),
    ('bg_onboarding_page_active', 'studyflow_primary', 3.5),
    ('bg_onboarding_page_inactive', 'studyflow_outline', 3.5),
]:
    write(f'res/drawable/{file}.xml', f'''
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="{radius}dp" />
    <solid android:color="@color/{color}" />
</shape>
''')

write('res/drawable/ic_onboarding_arrow.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="16dp"
    android:height="16dp"
    android:viewportWidth="16"
    android:viewportHeight="16">
    <path
        android:pathData="M2.166,8 H13.834 M8,13.834 L13.834,8 L8,2.166"
        android:fillColor="@android:color/transparent"
        android:strokeColor="@color/studyflow_white"
        android:strokeWidth="1"
        android:strokeLineCap="round" />
</vector>
''')

(MAIN/'res/drawable-xxhdpi').mkdir(parents=True, exist_ok=True)
shutil.copy2(Path(r'C:\Users\admin\Downloads\Academic illustration (4).png'), MAIN/'res/drawable-xxhdpi/onboarding_academic_illustration.png')
(MAIN/'res/font').mkdir(exist_ok=True)
with zipfile.ZipFile(HERE.parent/'splash-preparation/Inter-3.19.zip') as z:
    (MAIN/'res/font/inter_semibold.ttf').write_bytes(z.read('Inter Hinted for Windows/Desktop/Inter-SemiBold.ttf'))

manifest = (PROJECT/'app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
assert '.OnboardingActivity' not in manifest
write('AndroidManifest.xml', manifest.replace('    </application>', '''        <activity
            android:name=".OnboardingActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Onboarding" />
    </application>'''))

for p in PACKAGE.rglob('*.xml'):
    ET.parse(p)

def save_expected():
    expected = {}
    for p in PACKAGE.rglob('*'):
        if p.is_file():
            rel = p.relative_to(PACKAGE).as_posix()
            dest = PROJECT / rel
            expected[rel] = hashlib.sha256(dest.read_bytes()).hexdigest() if dest.exists() else None
    (HERE/'expected-source.json').write_text(json.dumps(expected, indent=2), encoding='utf-8')

save_expected()
print('Prepared onboarding source files.')
