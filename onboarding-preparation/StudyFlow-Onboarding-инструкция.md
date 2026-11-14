# StudyFlow — Onboarding «Track Every Deadline»

## 1. Анализ дизайна

Экран перенесён из вашего SVG 390 × 844. Использована ваша PNG-иллюстрация
1026 × 840 без изменений. Текст, кнопки, карточка-пример задания и индикаторы
созданы отдельными Android Views в XML.

| Элемент | Параметры макета |
|---|---|
| Боковые поля | 24dp |
| Иллюстрация с подложкой | 342 × 332, радиус 30 |
| Иллюстрация внутри карточки | 342 × 280 |
| Полупрозрачная карточка задания | 314 × 60, радиус 18 |
| Плашка над заголовком | 207 × 22, радиус 11 |
| Заголовок | Inter Bold, 32sp |
| Описание | Inter Regular, 14sp |
| Основной текст | #172443 |
| Вторичный текст | #66728B |
| Кнопка | #4564ED, высота 52dp, радиус 14 |

Верхний текст — Inter Bold 16sp; Skip — Inter Medium 13sp; Get Started —
Inter SemiBold 14sp. Ранее добавленные Inter Regular, Medium и Bold используются
повторно; добавлен только SemiBold. Синяя тень кнопки подготовлена из параметров
SVG: смещение 8, Gaussian blur sigma 10, непрозрачность 48/255.

Разметка Splash и его ресурсы сохранены без изменений. Добавлен временный
переход: через 1,2 секунды показа Splash открывается onboarding. При уходе
приложения в фон ожидающий переход отменяется. Возврат кнопкой Back из
onboarding закрывает этот экран; заставка не остаётся под ним в стеке.

Skip, Get Started и Log In пока дают только реакцию на нажатие. Переходы
к регистрации, авторизации и остальным onboarding-экранам ещё не подключены,
так как соответствующих реализованных экранов пока нет. Данные не сохраняются.

## 2. Какие файлы нужны

Папка проекта: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`.
Из существующих файлов изменены только `MainActivity.kt` и `AndroidManifest.xml`.
Все остальные файлы ниже — новые. Gradle и архитектура приложения не изменены.

- [app/src/main/AndroidManifest.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/AndroidManifest.xml>)
- [app/src/main/java/com/example/studyflowapp/MainActivity.kt](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/java/com/example/studyflowapp/MainActivity.kt>)
- [app/src/main/java/com/example/studyflowapp/OnboardingActivity.kt](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/java/com/example/studyflowapp/OnboardingActivity.kt>)
- [app/src/main/res/drawable/bg_onboarding_badge.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/bg_onboarding_badge.xml>)
- [app/src/main/res/drawable/bg_onboarding_deadline.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/bg_onboarding_deadline.xml>)
- [app/src/main/res/drawable/bg_onboarding_hero.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/bg_onboarding_hero.xml>)
- [app/src/main/res/drawable/bg_onboarding_page_active.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/bg_onboarding_page_active.xml>)
- [app/src/main/res/drawable/bg_onboarding_page_inactive.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/bg_onboarding_page_inactive.xml>)
- [app/src/main/res/drawable/ic_onboarding_arrow.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable/ic_onboarding_arrow.xml>)
- [app/src/main/res/drawable-xxhdpi/onboarding_academic_illustration.png](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable-xxhdpi/onboarding_academic_illustration.png>)
- [app/src/main/res/drawable-xxhdpi/onboarding_button_shadow.png](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable-xxhdpi/onboarding_button_shadow.png>)
- [app/src/main/res/font/inter_semibold.ttf](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/font/inter_semibold.ttf>)
- [app/src/main/res/layout/activity_onboarding.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/layout/activity_onboarding.xml>)
- [app/src/main/res/values/onboarding_colors.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/values/onboarding_colors.xml>)
- [app/src/main/res/values/onboarding_strings.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/values/onboarding_strings.xml>)
- [app/src/main/res/values/onboarding_styles.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/values/onboarding_styles.xml>)

## 3. Пошаговая инструкция

Файлы уже добавлены в проект. Повторно копировать код не нужно.

1. Откройте **StudyFlowApp** в Android Studio.
2. В верхней панели выберите **app** и **Medium Phone API 37.0**.
3. Нажмите зелёную кнопку **Run ▶**.
4. После системной заставки отобразится готовый Splash, затем новый onboarding.
5. Для изучения XML откройте **app → res → layout → activity_onboarding.xml**.
6. Для просмотра разметки рядом с кодом выберите **Split**.
7. Kotlin-код нового экрана находится в **app → kotlin+java →
   com.example.studyflowapp → OnboardingActivity**.

На небольшом экране или при увеличенном шрифте прокрутите страницу вверх,
чтобы добраться до Get Started и Log In. На размере макета всё помещается
без прокрутки. Прокрутка не добавляет новых видимых элементов интерфейса.

Для ручного восстановления этапа используйте архив `StudyFlowApp-onboarding.zip`.
Это дополнение к уже готовому проекту со Splash, а не отдельный Android-проект.
В архиве папка `app` соответствует папке `app` вашего проекта.

Kotlin-файлы создаются как **Kotlin Class/File**, XML — как **XML Resource File**
в указанной папке. Для бинарных ресурсов скопируйте готовые файлы из архива:
`inter_semibold.ttf` в `res/font`, обе PNG в `res/drawable-xxhdpi`.
XML-ресурсы в `values` создаются как **Values Resource File**.
Для `MainActivity.kt` и `AndroidManifest.xml` используйте полную замену содержимого
версиями ниже; остальные файлы создайте с указанными именами.

## 4. Готовый код

### AndroidManifest.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\AndroidManifest.xml`

**Действие:** Заменить содержимое существующего файла.

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
        <activity
            android:name=".OnboardingActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Onboarding" />
    </application>

</manifest>

```

### MainActivity.kt

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\MainActivity.kt`

**Действие:** Заменить содержимое существующего файла.

```kotlin
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

```

### OnboardingActivity.kt

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\OnboardingActivity.kt`

**Действие:** Создать новый файл и вставить весь код.

```kotlin
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

```

### bg_onboarding_badge.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_onboarding_badge.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="11dp" />
    <solid android:color="@color/studyflow_badge_background" />
</shape>

```

### bg_onboarding_deadline.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_onboarding_deadline.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="18dp" />
    <solid android:color="#D9FFFFFF" />
    <stroke android:width="1dp" android:color="@color/studyflow_white" />
</shape>

```

### bg_onboarding_hero.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_onboarding_hero.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
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

```

### bg_onboarding_page_active.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_onboarding_page_active.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="3.5dp" />
    <solid android:color="@color/studyflow_primary" />
</shape>

```

### bg_onboarding_page_inactive.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_onboarding_page_inactive.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="3.5dp" />
    <solid android:color="@color/studyflow_outline" />
</shape>

```

### ic_onboarding_arrow.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_onboarding_arrow.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
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

```

### activity_onboarding.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_onboarding.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
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

```

### onboarding_colors.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\onboarding_colors.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="studyflow_ink">#172443</color>
    <color name="studyflow_muted">#66728B</color>
    <color name="studyflow_primary">#4564ED</color>
    <color name="studyflow_outline">#E5EAF3</color>
    <color name="studyflow_badge_background">#EDF1FF</color>
</resources>

```

### onboarding_strings.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\onboarding_strings.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
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

```

### onboarding_styles.xml

**Файл:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\onboarding_styles.xml`

**Действие:** Создать новый файл и вставить весь код.

```xml
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

```

## 5. Проверка

- `assembleDebug` и `lintDebug` завершились успешно.
- Ошибок Lint: **0**. Предупреждений: **8**.
- Запуск проверен на эмуляторе API 37; Splash автоматически открывает onboarding.
- При размере 390 × 844dp карточка занимает точные координаты SVG:
  x = 24, y = 116, ширина = 342, высота = 332.
- Проверен экран 360 × 640dp со шрифтом 130%: кнопка и Log In доступны после прокрутки.
- Нажатие Get Started оставляет пользователя на onboarding, как запланировано на этом этапе.
- Исходные размер, плотность и масштаб текста эмулятора восстановлены после проверки.
- Сверены 15 файлов ресурсов Splash: их содержимое не изменилось.

Отдельного запуска на Android 7 не было; minSdk 24 проверен сборкой и Lint.
Скругление иллюстрации включается через Kotlin API, доступный на этой версии Android.

Предупреждения:

- `VectorRaster`: Limit vector icons sizes to 200×200 to keep icon drawing fast; see https://developer.android.com/studio/write/vector-asset-studio#when for more
- `VectorRaster`: Limit vector icons sizes to 200×200 to keep icon drawing fast; see https://developer.android.com/studio/write/vector-asset-studio#when for more
- `AndroidGradlePluginVersion`: A newer version of com.android.application than 9.4.1 is available: 9.5.0
- `UnusedResources`: The resource `R.color.black` appears to be unused
- `UnusedResources`: The resource `R.color.white` appears to be unused
- `IconMissingDensityFolder`: Missing density variation folders in `src\main\res`: drawable-hdpi, drawable-mdpi, drawable-xhdpi
- `SmallSp`: Avoid using sizes smaller than `11sp`: `10sp`
- `SmallSp`: Avoid using sizes smaller than `11sp`: `10sp`

Размеры 10sp в подписи иллюстрации и плашке сохранены из вашего макета.
Lint рекомендует более крупный текст, но самовольно менять дизайн я не стал.
Остальные предупреждения относятся к ресурсам и версии инструментов проекта.

Снимки рядом с этой инструкцией:

- `StudyFlow-Onboarding-emulator.png` — обычный размер вашего эмулятора.
- `Onboarding-390x844.png` — сравнение с макетом при 390 × 844dp, снимок в масштабе 3×.
- `Onboarding-small-font130.png` — небольшой экран с увеличенным текстом после прокрутки.

Время, батарея и нижняя жестовая полоска отображаются самой системой Android.
Они отличаются от нарисованных системных панелей iPhone в Figma.

Источник шрифта: [Inter 3.19](https://github.com/rsms/inter/releases/tag/v3.19).
Лицензия уже находится в `app/src/main/assets/licenses/inter_ofl.txt` со стадии Splash.
Основная кнопка использует существующий [MaterialButton](https://developer.android.com/reference/com/google/android/material/button/MaterialButton)
из зависимости Material проекта. Новых библиотек не установлено.
