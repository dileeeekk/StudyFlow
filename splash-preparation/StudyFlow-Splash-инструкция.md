# StudyFlow — экран Splash

## 1. Анализ дизайна

Основа — экспортированный вами фрейм Figma 390 × 844. Градиент имеет цвета
`#273D86`, `#4969E8`, `#9672D6` с точками 0%, 55%, 100%. Нижний круг имеет
центр (135, 665) и радиус 275; верхний — центр (415, 105) и радиус 225.
Подложка логотипа — 96 × 96, радиус скругления — 28. Иконка переведена
из вашего SVG в Android VectorDrawable. Тень сохранена отдельным PNG.

Текст остаётся настоящими TextView: Inter Bold 40sp, Inter Regular 16sp,
Inter Medium 11sp. Шрифт включён в приложение, поэтому сеть для его показа
не нужна. Все три точки статичны; переходы и таймеры пока не добавлены.

Фон занимает весь экран, включая области за системными панелями. Время,
сеть, батарея и жестовая полоска принадлежат Android: они показывают
настоящие данные и могут отличаться от iPhone-панелей на макете. Скруглённые
углы устройства определяются его экраном, поэтому фон приложения не обрезан
искусственно по радиусу 32.

## 2. Какие файлы нужны

Из существующих файлов изменены только `MainActivity.kt`, `activity_main.xml`
и `AndroidManifest.xml`. Остальные перечисленные ниже файлы добавлены.
Gradle, исходные themes.xml и зависимости проекта не изменены.
Точная папка проекта: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`.

- [app/src/main/AndroidManifest.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/AndroidManifest.xml>)
- [app/src/main/assets/licenses/inter_ofl.txt](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/assets/licenses/inter_ofl.txt>)
- [app/src/main/java/com/example/studyflowapp/MainActivity.kt](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/java/com/example/studyflowapp/MainActivity.kt>)
- [app/src/main/res/drawable/bg_studyflow_dot.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/bg_studyflow_dot.xml>)
- [app/src/main/res/drawable/bg_studyflow_splash.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/bg_studyflow_splash.xml>)
- [app/src/main/res/drawable/ic_studyflow_launch.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/ic_studyflow_launch.xml>)
- [app/src/main/res/drawable/ic_studyflow_logo.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/ic_studyflow_logo.xml>)
- [app/src/main/res/drawable/studyflow_logo.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/studyflow_logo.xml>)
- [app/src/main/res/drawable-xxhdpi/studyflow_logo_shadow.png](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable-xxhdpi/studyflow_logo_shadow.png>)
- [app/src/main/res/font/inter_bold.ttf](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/font/inter_bold.ttf>)
- [app/src/main/res/font/inter_medium.ttf](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/font/inter_medium.ttf>)
- [app/src/main/res/font/inter_regular.ttf](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/font/inter_regular.ttf>)
- [app/src/main/res/layout/activity_main.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/layout/activity_main.xml>)
- [app/src/main/res/values/studyflow_colors.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/values/studyflow_colors.xml>)
- [app/src/main/res/values/studyflow_splash_theme.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/values/studyflow_splash_theme.xml>)
- [app/src/main/res/values/studyflow_strings.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/values/studyflow_strings.xml>)
- [app/src/main/res/values-v31/studyflow_splash_theme.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/values-v31/studyflow_splash_theme.xml>)

## 3. Пошаговая инструкция

Подготовленные файлы уже установлены в ваш проект. Повторно вставлять код не нужно.

1. Откройте **StudyFlowApp** в Android Studio.
2. Слева выберите представление **Android**.
3. Откройте **app → res → layout → activity_main.xml**.
4. В редакторе выберите **Split** или **Design**, чтобы увидеть предварительный просмотр.
5. Kotlin-код находится в **app → kotlin+java → com.example.studyflowapp → MainActivity**.
6. Дождитесь окончания индексации ресурсов, если Android Studio ещё обрабатывает изменения.

Если нужно восстановить этот этап вручную, распакуйте `StudyFlowApp-splash.zip`.
В архиве находится папка `app`: её содержимое соответствует папке `app` вашего
проекта. XML-файлы создаются как обычные XML resource files в указанных папках,
Kotlin-файл — как Kotlin Class/File. В `res/font` копируются готовые TTF-файлы,
в `res/drawable-xxhdpi` — PNG тени. Код бинарных файлов вручную вводить не нужно.
Существующие три текстовых файла можно полностью заменить версиями ниже.
Для новых текстовых файлов создайте файл с точным именем и вставьте весь его код.

## 4. Готовый код

Ниже приведены полные версии всех изменённых и добавленных XML/Kotlin-файлов.
Шрифты, PNG и текст лицензии входят в архив.

### AndroidManifest.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\AndroidManifest.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.StudyFlowApp">
        <activity
            android:name=".MainActivity"
            android:theme="@style/Theme.StudyFlowApp.Splash"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```

### MainActivity.kt

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\MainActivity.kt`

```kotlin
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
```

### bg_studyflow_dot.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_studyflow_dot.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="oval">
    <solid android:color="@color/studyflow_white" />
</shape>
```

### bg_studyflow_splash.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_studyflow_splash.xml`

```xml
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
```

### ic_studyflow_launch.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_studyflow_launch.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="288dp"
    android:height="288dp"
    android:viewportWidth="288"
    android:viewportHeight="288">
    <group android:translateX="56" android:translateY="68">

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
        android:pathData="M87.9996 94V66M87.9996 94C87.9996 92.4087 87.3675 90.8826 86.2421 89.7574C85.1168 88.6321 83.5906 88 81.9992 88H69.9982C69.4677 88 68.959 87.7893 68.5839 87.4142C68.2088 87.0391 67.998 86.5304 67.998 86V60C67.998 59.4696 68.2088 58.9609 68.5839 58.5858C68.959 58.2107 69.4677 58 69.9982 58H79.999C82.1209 58 84.1559 58.8429 85.6563 60.3431C87.1567 61.8434 87.9996 63.8783 87.9996 66M87.9996 94C87.9996 92.4087 88.6318 90.8826 89.7571 89.7574C90.8825 88.6321 92.4087 88 94.0001 88H106.001C106.532 88 107.04 87.7893 107.415 87.4142C107.791 87.0391 108.001 86.5304 108.001 86V83.4M87.9996 66C87.9996 63.8783 88.8426 61.8434 90.343 60.3431C91.8434 58.8429 93.8784 58 96.0003 58H106.001C106.532 58 107.04 58.2107 107.415 58.5858C107.791 58.9609 108.001 59.4696 108.001 60V64M96.0003 76L100.001 80L108.001 72" />

    </group>
</vector>
```

### ic_studyflow_logo.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_studyflow_logo.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="176dp"
    android:height="176dp"
    android:viewportWidth="176"
    android:viewportHeight="176">

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
        android:pathData="M87.9996 94V66M87.9996 94C87.9996 92.4087 87.3675 90.8826 86.2421 89.7574C85.1168 88.6321 83.5906 88 81.9992 88H69.9982C69.4677 88 68.959 87.7893 68.5839 87.4142C68.2088 87.0391 67.998 86.5304 67.998 86V60C67.998 59.4696 68.2088 58.9609 68.5839 58.5858C68.959 58.2107 69.4677 58 69.9982 58H79.999C82.1209 58 84.1559 58.8429 85.6563 60.3431C87.1567 61.8434 87.9996 63.8783 87.9996 66M87.9996 94C87.9996 92.4087 88.6318 90.8826 89.7571 89.7574C90.8825 88.6321 92.4087 88 94.0001 88H106.001C106.532 88 107.04 87.7893 107.415 87.4142C107.791 87.0391 108.001 86.5304 108.001 86V83.4M87.9996 66C87.9996 63.8783 88.8426 61.8434 90.343 60.3431C91.8434 58.8429 93.8784 58 96.0003 58H106.001C106.532 58 107.04 58.2107 107.415 58.5858C107.791 58.9609 108.001 59.4696 108.001 60V64M96.0003 76L100.001 80L108.001 72" />

</vector>
```

### studyflow_logo.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\studyflow_logo.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item>
        <bitmap android:src="@drawable/studyflow_logo_shadow" android:gravity="fill" />
    </item>
    <item android:drawable="@drawable/ic_studyflow_logo" />
</layer-list>
```

### activity_main.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_main.xml`

```xml
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
        android:layout_marginStart="24dp"
        android:layout_marginEnd="24dp"
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
        android:layout_marginStart="24dp"
        android:layout_marginEnd="24dp"
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
        android:layout_marginStart="24dp"
        android:layout_marginEnd="24dp"
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
```

### studyflow_colors.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\studyflow_colors.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="studyflow_blue_start">#273D86</color>
    <color name="studyflow_blue_middle">#4969E8</color>
    <color name="studyflow_lilac_end">#9672D6</color>
    <color name="studyflow_white">#FFFFFF</color>
    <color name="studyflow_subtitle">#E5FFFFFF</color>
    <color name="studyflow_tagline">#BBFFFFFF</color>
</resources>
```

### studyflow_splash_theme.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\studyflow_splash_theme.xml`

```xml
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
```

### studyflow_strings.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\studyflow_strings.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="studyflow_splash_title" translatable="false">StudyFlow</string>
    <string name="studyflow_splash_subtitle">Organize Your Academic Life</string>
    <string name="studyflow_splash_tagline">LESS CHAOS. MORE FLOW.</string>
</resources>
```

### studyflow_splash_theme.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values-v31\studyflow_splash_theme.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.StudyFlowApp.Splash" parent="Base.Theme.StudyFlowApp.Splash">
        <item name="android:windowSplashScreenBackground">@color/studyflow_blue_start</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/ic_studyflow_launch</item>
        <item name="android:windowSplashScreenAnimationDuration">0</item>
    </style>
</resources>
```

## 5. Проверка

1. В верхней панели Android Studio выберите устройство **Medium Phone API 37.0**.
2. Рядом должна быть конфигурация **app**.
3. Нажмите зелёный треугольник **Run ▶**.
4. После краткого системного экрана запуска должен появиться градиентный экран:
   книга с галочкой, StudyFlow, английская подпись, три точки и нижний слоган.
5. Экран остаётся открытым: это запланированное поведение текущего этапа вёрстки.

На Android 12 и новее перед разметкой Activity появляется системная заставка.
Для неё уже заданы синий фон и логотип StudyFlow. Полный градиентный макет
отображается после запуска Activity; искусственной задержки нет.

Проверено: `assembleDebug` и `lintDebug` завершились успешно; ошибок Lint нет.
Осталось 6 предупреждений: два о размере статичных векторов, одно о наличии новой
версии Gradle-плагина, два о неиспользуемых цветах исходного шаблона и одно
о недостающих вариантах плотности PNG. Android масштабирует имеющийся вариант
тени xxhdpi; эти предупреждения не мешают сборке. Версия Gradle-плагина не менялась.

Приложение установлено и запущено в эмуляторе API 37, 1080 × 2400, density 420.
Повторный холодный запуск завершился с `Status: ok`, без ошибки приложения.
Фактический снимок сохранён рядом с инструкцией: `StudyFlow-Splash-emulator.png`.
На API 24 выполнена только проверка совместимости сборкой и Lint: отдельный
запуск на устройстве с этой версией Android не проводился.

На прозрачной нижней панели Android может автоматически менять цвет жестовой
полоски в зависимости от фона. Поэтому на проверенном эмуляторе она тёмная.
Это [поведение системной панели Android](https://developer.android.com/design/ui/mobile/guides/foundations/system-bars),
а не дополнительный элемент в XML-разметке.

На устройствах с другими пропорциями высота фона и положение направляющих
адаптируются. Размеры логотипа и отступов заданы в dp, текст — в sp.
Для сравнения с Figma используйте стандартный масштаб текста.

Источник шрифта: [официальный релиз Inter 3.19](https://github.com/rsms/inter/releases/tag/v3.19).
Лицензия SIL Open Font License приложена в `app/src/main/assets/licenses/inter_ofl.txt`.
Метрики этой версии сопоставлены с контурным SVG: ширина StudyFlow примерно
208 единиц, а подписи — 217.4. Необычные значения letter-spacing из текстового
экспорта SVG не перенесены буквально, поскольку они противоречат расположению
букв в исходном контурном SVG. Использован обычный кернинг Inter.
