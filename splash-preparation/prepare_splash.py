from pathlib import Path
import shutil
import hashlib
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'StudyFlowApp-splash'
SOURCE = Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
MAIN = PACKAGE / 'app/src/main'

def write(relative, text):
    dest = MAIN / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    text = text.replace('android:layout_marginHorizontal="24dp"', 'android:layout_marginStart="24dp"\n        android:layout_marginEnd="24dp"')
    dest.write_text(text.strip() + '\n', encoding='utf-8')

write('java/com/example/studyflowapp/MainActivity.kt', '''
package com.example.studyflowapp

import android.graphics.Color
import android.os.Bundle
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // The gradient continues behind Android's white system icons.
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.dark(Color.TRANSPARENT)
        )

        setContentView(R.layout.activity_main)
    }
}
''')

write('res/layout/activity_main.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@drawable/bg_studyflow_splash"
    android:clipChildren="false"
    android:clipToPadding="false"
    tools:context=".MainActivity">

    <!-- 284.5 / 844: logo position in the Figma frame. -->
    <androidx.constraintlayout.widget.Guideline
        android:id="@+id/splash_logo_guide"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        app:layout_constraintGuide_percent="0.3370853" />

    <FrameLayout
        android:id="@+id/splash_logo"
        android:layout_width="96dp"
        android:layout_height="96dp"
        android:clipChildren="false"
        android:clipToPadding="false"
        android:importantForAccessibility="noHideDescendants"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="@id/splash_logo_guide">

        <!-- The extra transparent space contains the original soft shadow. -->
        <ImageView
            android:layout_width="176dp"
            android:layout_height="176dp"
            android:layout_gravity="center"
            android:contentDescription="@null"
            android:scaleType="fitXY"
            android:src="@drawable/studyflow_logo"
            android:translationY="12dp" />
    </FrameLayout>

    <TextView
        android:id="@+id/splash_title"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginHorizontal="24dp"
        android:layout_marginTop="24dp"
        android:fontFamily="@font/inter_bold"
        android:gravity="center"
        android:includeFontPadding="false"
        android:letterSpacing="0"
        android:minHeight="48dp"
        android:text="@string/studyflow_splash_title"
        android:textColor="@color/studyflow_white"
        android:textSize="40sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/splash_logo" />

    <TextView
        android:id="@+id/splash_subtitle"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginHorizontal="24dp"
        android:layout_marginTop="11dp"
        android:fontFamily="@font/inter_regular"
        android:gravity="center"
        android:includeFontPadding="false"
        android:letterSpacing="0"
        android:minHeight="20dp"
        android:text="@string/studyflow_splash_subtitle"
        android:textColor="@color/studyflow_subtitle"
        android:textSize="16sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/splash_title" />

    <!-- 720 / 844: top of the three decorative dots. -->
    <androidx.constraintlayout.widget.Guideline
        android:id="@+id/splash_footer_guide"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        app:layout_constraintGuide_percent="0.8530806" />

    <LinearLayout
        android:id="@+id/splash_dots"
        android:layout_width="wrap_content"
        android:layout_height="5dp"
        android:importantForAccessibility="noHideDescendants"
        android:orientation="horizontal"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="@id/splash_footer_guide">

        <View
            android:layout_width="5dp"
            android:layout_height="5dp"
            android:background="@drawable/bg_studyflow_dot" />

        <View
            android:layout_width="5dp"
            android:layout_height="5dp"
            android:layout_marginStart="6dp"
            android:alpha="0.333333"
            android:background="@drawable/bg_studyflow_dot" />

        <View
            android:layout_width="5dp"
            android:layout_height="5dp"
            android:layout_marginStart="6dp"
            android:alpha="0.333333"
            android:background="@drawable/bg_studyflow_dot" />
    </LinearLayout>

    <TextView
        android:id="@+id/splash_tagline"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginHorizontal="24dp"
        android:layout_marginTop="12dp"
        android:fontFamily="@font/inter_medium"
        android:gravity="center"
        android:includeFontPadding="false"
        android:letterSpacing="0"
        android:text="@string/studyflow_splash_tagline"
        android:textColor="@color/studyflow_tagline"
        android:textSize="11sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@id/splash_dots" />

</androidx.constraintlayout.widget.ConstraintLayout>
''')

write('res/values/studyflow_colors.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="studyflow_blue_start">#273D86</color>
    <color name="studyflow_blue_middle">#4969E8</color>
    <color name="studyflow_lilac_end">#9672D6</color>
    <color name="studyflow_white">#FFFFFF</color>
    <color name="studyflow_subtitle">#E5FFFFFF</color>
    <color name="studyflow_tagline">#BBFFFFFF</color>
</resources>
''')

write('res/values/studyflow_strings.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="studyflow_splash_title" translatable="false">StudyFlow</string>
    <string name="studyflow_splash_subtitle">Organize Your Academic Life</string>
    <string name="studyflow_splash_tagline">LESS CHAOS. MORE FLOW.</string>
</resources>
''')

write('res/drawable/bg_studyflow_splash.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:aapt="http://schemas.android.com/aapt"
    android:width="390dp"
    android:height="844dp"
    android:viewportWidth="390"
    android:viewportHeight="844">

    <path android:pathData="M0,0 H390 V844 H0 Z">
        <aapt:attr name="android:fillColor">
            <gradient
                android:type="linear"
                android:startX="0"
                android:startY="0"
                android:endX="0"
                android:endY="844">
                <item android:offset="0" android:color="@color/studyflow_blue_start" />
                <item android:offset="0.55" android:color="@color/studyflow_blue_middle" />
                <item android:offset="1" android:color="@color/studyflow_lilac_end" />
            </gradient>
        </aapt:attr>
    </path>

    <path
        android:fillColor="#16B9C5FF"
        android:pathData="M-140,665 A275,275 0,1 1,410 665 A275,275 0,1 1,-140 665 Z" />

    <path
        android:fillColor="#0AFFFFFF"
        android:pathData="M190,105 A225,225 0,1 1,640 105 A225,225 0,1 1,190 105 Z" />

    <path
        android:fillColor="@android:color/transparent"
        android:strokeColor="#14FFFFFF"
        android:strokeWidth="1"
        android:pathData="M190.5,105 A224.5,224.5 0,1 1,639.5 105 A224.5,224.5 0,1 1,190.5 105 Z" />
</vector>
''')

write('res/drawable/bg_studyflow_dot.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="oval">
    <solid android:color="@color/studyflow_white" />
</shape>
''')

ns = {'s': 'http://www.w3.org/2000/svg'}
logo = ET.parse(Path(r'C:\Users\admin\Downloads\StudyFlow logo (1).svg'))
book = logo.find('.//s:path', ns).attrib['d']
logo_paths = f'''
    <path
        android:fillColor="#24FFFFFF"
        android:pathData="M68,28 H108 A28,28 0,0 1,136 56 V96 A28,28 0,0 1,108 124 H68 A28,28 0,0 1,40 96 V56 A28,28 0,0 1,68 28 Z" />
    <path
        android:fillColor="@android:color/transparent"
        android:strokeColor="#66FFFFFF"
        android:strokeWidth="1.5"
        android:pathData="M68,28.75 H108 A27.25,27.25 0,0 1,135.25 56 V96 A27.25,27.25 0,0 1,108 123.25 H68 A27.25,27.25 0,0 1,40.75 96 V56 A27.25,27.25 0,0 1,68 28.75 Z" />
    <path
        android:fillColor="@android:color/transparent"
        android:strokeColor="@color/studyflow_white"
        android:strokeWidth="1"
        android:strokeLineCap="round"
        android:strokeLineJoin="miter"
        android:pathData="{book}" />
'''
write('res/drawable/ic_studyflow_logo.xml', f'''
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="176dp"
    android:height="176dp"
    android:viewportWidth="176"
    android:viewportHeight="176">
{logo_paths}
</vector>
''')

write('res/drawable/studyflow_logo.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item>
        <bitmap android:src="@drawable/studyflow_logo_shadow" android:gravity="fill" />
    </item>
    <item android:drawable="@drawable/ic_studyflow_logo" />
</layer-list>
''')

write('res/drawable/ic_studyflow_launch.xml', f'''
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="288dp"
    android:height="288dp"
    android:viewportWidth="288"
    android:viewportHeight="288">
    <group android:translateX="56" android:translateY="68">
{logo_paths}
    </group>
</vector>
''')

write('res/values/studyflow_splash_theme.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Base.Theme.StudyFlowApp.Splash" parent="Theme.StudyFlowApp">
        <item name="android:windowBackground">@color/studyflow_blue_start</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:statusBarColor">@android:color/transparent</item>
        <item name="android:navigationBarColor">@android:color/transparent</item>
    </style>
    <style name="Theme.StudyFlowApp.Splash" parent="Base.Theme.StudyFlowApp.Splash" />
</resources>
''')

write('res/values-v31/studyflow_splash_theme.xml', '''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.StudyFlowApp.Splash" parent="Base.Theme.StudyFlowApp.Splash">
        <item name="android:windowSplashScreenBackground">@color/studyflow_blue_start</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/ic_studyflow_launch</item>
        <item name="android:windowSplashScreenAnimationDuration">0</item>
    </style>
</resources>
''')

manifest = (SOURCE/'app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
assert 'android:name=".MainActivity"' in manifest
write('AndroidManifest.xml', manifest.replace('android:name=".MainActivity"', 'android:name=".MainActivity"\n            android:theme="@style/Theme.StudyFlowApp.Splash"'))

for weight in ['Regular', 'Medium', 'Bold']:
    shutil.copy2(HERE/'font-check'/f'Inter-{weight}.ttf', MAIN/'res/font'/f'inter_{weight.lower()}.ttf')
shutil.copy2(HERE/'font-check/OFL.txt', MAIN/'assets/licenses/inter_ofl.txt')

# Parse every resource before attempting an Android build.
for file in PACKAGE.rglob('*.xml'):
    ET.parse(file)
print(f'Prepared {sum(1 for p in PACKAGE.rglob("*") if p.is_file())} files in {PACKAGE}')

expected = {}
for file in PACKAGE.rglob('*'):
    if file.is_file():
        relative = file.relative_to(PACKAGE).as_posix()
        target = SOURCE / relative
        expected[relative] = hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None
(HERE/'expected-source.json').write_text(json.dumps(expected, indent=2), encoding='utf-8')
