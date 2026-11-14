# StudyFlowApp — экран Login

## 1. Анализ дизайна

Экран собран по Login.svg и Brand mark.svg: белый фон, логотип 56×56 dp, заголовок Inter Bold 34 sp, подзаголовок, карточка формы 342×320 dp при ширине экрана 390 dp, два поля 52 dp, чекбокс, ссылка восстановления пароля, кнопка Log In и нижние ссылки. Цвета и шрифты переиспользованы из предыдущих экранов.

Верхняя строка состояния и нижняя полоса жестов принадлежат Android. Их значки, время и оттенок полосы могут отличаться от iOS-макета; второй набор системных значков не нарисован.

## 2. Какие файлы нужны

Изменения уже установлены в ваш проект. Вручную копировать код сейчас не требуется.

Из прежних файлов изменены только AndroidManifest.xml (регистрация LoginActivity) и OnboardingActivity.kt (переходы). MainActivity, splash и разметки предыдущих экранов сохранены.

Полный список файлов этого этапа:


- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\AndroidManifest.xml` — изменён.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\LoginActivity.kt` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\OnboardingActivity.kt` — изменён.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_login_brand.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_login_card.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_login_field.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_brand.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_checked.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_email.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_eye.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_eye_off.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_unchecked.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\login_checkbox.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\login_button_shadow.png` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\login_card_shadow.png` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_login.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\login_strings.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\login_styles.xml` — создан.


## 3. Пошаговая инструкция

1. Открой Android Studio и проект `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`.
2. Вверху выбери конфигурацию **app** и свой эмулятор.
3. Нажми зелёный треугольник **Run**. Если приложение уже открыто, запуск через Run покажет начальную последовательность экранов.
4. После splash на любом onboarding нажми **Log In** или **Skip**. Также Login открывается по **Get Started** на последнем onboarding.
5. Нажми поле, чтобы открыть клавиатуру. Введи любой тестовый текст. Значок глаза показывает и скрывает введённый пароль; Remember me переключается.
6. **Log In** закрывает клавиатуру и остаётся на этом экране. Восстановление пароля и создание аккаунта пока дают только визуальную реакцию на касание. Их экраны добавим по следующим макетам.
7. Системная кнопка/жест «Назад» возвращает к тому onboarding, с которого открыт Login.

Адрес email и точки пароля из макета показаны как подсказки. Поля изначально пустые. Авторизация, запросы и сохранение учётных данных не добавлены; Remember me пока управляет только своим состоянием на экране.

Если нужно перенести этот этап в копию того же проекта: распакуй `StudyFlowApp-login.zip` и скопируй его папку `app` в корень проекта, объединив папки. Архив содержит только файлы этого этапа и требует ресурсы уже созданных экранов. Для двух заменяемых файлов сохранена резервная копия в папке `login/backup` рядом с этой инструкцией.

## 4. Готовый код

Ниже полный код каждого текстового файла. Если восстанавливаешь файл вручную: открой указанный путь, выдели содержимое целиком и вставь соответствующий код. Не заменяй другие файлы проекта.

Для нового XML в папке `res/layout`, `res/drawable` или `res/values`: нажми по папке правой кнопкой → **New → Layout Resource File / Drawable Resource File / Values Resource File**, укажи имя без `.xml`, затем переключись в **Code** и вставь полный код.

Для Kotlin: открой пакет `com.example.studyflowapp` в основной группе `kotlin+java` (без test/androidTest), выбери **New → Kotlin Class/File → File**, имя `LoginActivity`.

PNG-тени уже подготовлены по параметрам SVG. Их не нужно создавать как XML: скопируй готовые PNG из архива в папку `app/src/main/res/drawable-xxhdpi`. Если папки нет, создай её через **New → Android Resource Directory**, Resource type `drawable`, Density `XX-High Density`.


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\AndroidManifest.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


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
        <activity
            android:name=".LoginActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Login"
            android:windowSoftInputMode="adjustResize|stateAlwaysHidden" />
    </application>

</manifest>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\LoginActivity.kt`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```kotlin
package com.example.studyflowapp

import android.graphics.Color
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
import androidx.core.widget.NestedScrollView

class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.rgb(23, 36, 67))
        )
        setContentView(R.layout.activity_login)
        val scroll = findViewById<NestedScrollView>(R.id.login_scroll)
        findViewById<View>(R.id.login_content).requestFocus()
        fun revealFocusedField() {
            val field = currentFocus as? EditText ?: return
            scroll.post {
                val fieldPosition = IntArray(2)
                val scrollPosition = IntArray(2)
                field.getLocationOnScreen(fieldPosition)
                scroll.getLocationOnScreen(scrollPosition)
                val visibleBottom = scrollPosition[1] + scroll.height - scroll.paddingBottom - dp(12)
                val overlap = fieldPosition[1] + field.height - visibleBottom
                if (overlap > 0) scroll.smoothScrollBy(0, overlap)
            }
        }
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
                revealFocusedField()
            }
            previousImeBottom = ime.bottom
            insets
        }
        ViewCompat.requestApplyInsets(scroll)

        val password = findViewById<EditText>(R.id.login_password)
        val email = findViewById<EditText>(R.id.login_email)
        for (field in listOf(email, password)) {
            field.setOnFocusChangeListener { _, focused ->
                if (focused && previousImeBottom > 0) revealFocusedField()
            }
        }
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
            findViewById<View>(R.id.login_content).requestFocus()
        }
        // UI preview only: no credential validation, storage or network requests.
        findViewById<View>(R.id.login_submit).setOnClickListener { closeKeyboard() }
        password.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) { closeKeyboard(); true } else false
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\OnboardingActivity.kt`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```kotlin
package com.example.studyflowapp

import android.content.Intent
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
    private var openingNextPage = false

    private companion object {
        const val EXTRA_PAGE_INDEX = "com.example.studyflowapp.ONBOARDING_PAGE"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(
                Color.TRANSPARENT,
                Color.rgb(23, 36, 67)
            )
        )
        val pageIndex = intent.getIntExtra(EXTRA_PAGE_INDEX, 0).coerceIn(0, 2)
        setContentView(
            when (pageIndex) {
                1 -> R.layout.activity_onboarding_classes
                2 -> R.layout.activity_onboarding_focus
                else -> R.layout.activity_onboarding
            }
        )

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
        // Temporary navigation between the three completed onboarding layouts.
        if (pageIndex < 2) {
            findViewById<View>(R.id.onboarding_get_started).setOnClickListener {
                if (!openingNextPage) {
                    openingNextPage = true
                    startActivity(
                        Intent(this, OnboardingActivity::class.java)
                            .putExtra(EXTRA_PAGE_INDEX, pageIndex + 1)
                    )
                }
            }
        }
        else {
            findViewById<View>(R.id.onboarding_get_started).setOnClickListener { openLogin() }
        }
        login.setOnClickListener { openLogin() }
        findViewById<View>(R.id.onboarding_skip).setOnClickListener { openLogin() }
    }

    private fun openLogin() {
        if (!openingNextPage) {
            openingNextPage = true
            startActivity(Intent(this, LoginActivity::class.java))
        }
    }

    override fun onResume() {
        super.onResume()
        openingNextPage = false
    }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density + 0.5f).toInt()
}
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_login_brand.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <corners android:radius="18dp" />
    <gradient android:angle="270" android:startColor="#EDF2FF" android:centerColor="#F5F6FD" android:centerY="0.6" android:endColor="#EAE3FA" />
</shape>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_login_card.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/studyflow_white" />
    <corners android:radius="22dp" />
    <stroke android:width="1dp" android:color="@color/studyflow_outline" />
</shape>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_login_field.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_focused="true"><shape><solid android:color="@color/studyflow_white" /><corners android:radius="14dp" /><stroke android:width="1dp" android:color="@color/studyflow_primary" /></shape></item>
    <item><shape><solid android:color="@color/studyflow_white" /><corners android:radius="14dp" /><stroke android:width="1dp" android:color="@color/studyflow_outline" /></shape></item>
</selector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_brand.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="56dp" android:height="56dp" android:viewportWidth="56" android:viewportHeight="56">
    <group android:translateX="0" android:translateY="0">
        <path android:pathData="M28 39.25V21.75M28 39.25C28 38.2554 27.6049 37.3016 26.9016 36.5983C26.1983 35.8951 25.2444 35.5 24.2497 35.5H16.7491C16.4176 35.5 16.0996 35.3683 15.8652 35.1339C15.6307 34.8995 15.499 34.5815 15.499 34.25V18C15.499 17.6685 15.6307 17.3505 15.8652 17.1161C16.0996 16.8817 16.4176 16.75 16.7491 16.75H22.9996C24.3258 16.75 25.5977 17.2768 26.5354 18.2145C27.4732 19.1521 28 20.4239 28 21.75M28 39.25C28 38.2554 28.3951 37.3016 29.0985 36.5983C29.8018 35.8951 30.7557 35.5 31.7503 35.5H39.2509C39.5825 35.5 39.9004 35.3683 40.1349 35.1339C40.3693 34.8995 40.501 34.5815 40.501 34.25V32.625M28 21.75C28 20.4239 28.5268 19.1521 29.4646 18.2145C30.4024 17.2768 31.6742 16.75 33.0004 16.75H39.2509C39.5825 16.75 39.9004 16.8817 40.1349 17.1161C40.3693 17.3505 40.501 17.6685 40.501 18V20.5M33.0004 28L35.5006 30.5L40.501 25.5" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_primary" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_checked.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="18dp" android:height="18dp" android:viewportWidth="18" android:viewportHeight="18">
    <group android:translateX="-44" android:translateY="-574">
        <path android:pathData="M50.75 583L52.25 584.5L55.25 581.5M47.75 576.25H58.25C59.0784 576.25 59.75 576.922 59.75 577.75V588.25C59.75 589.078 59.0784 589.75 58.25 589.75H47.75C46.9216 589.75 46.25 589.078 46.25 588.25V577.75C46.25 576.922 46.9216 576.25 47.75 576.25Z" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_primary" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_email.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="19dp" android:height="19dp" android:viewportWidth="19" android:viewportHeight="19">
    <group android:translateX="-313" android:translateY="-423.5">
        <path android:pathData="M330.418 429.042L323.299 433.576C323.058 433.716 322.783 433.79 322.504 433.79C322.225 433.79 321.95 433.716 321.709 433.576L314.583 429.042M330.418 429.042V428.251C330.418 427.376 329.709 426.667 328.834 426.667H316.166C315.292 426.667 314.583 427.376 314.583 428.251V429.042M330.418 429.042V437.75C330.418 438.624 329.709 439.333 328.834 439.333H316.166C315.292 439.333 314.583 438.624 314.583 437.75V429.042" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_muted" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_eye.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="19dp" android:height="19dp" android:viewportWidth="19" android:viewportHeight="19">
    <group android:translateX="0" android:translateY="0">
        <path android:pathData="M1.632,9.224 C3.0,5.9 6.1,4 9.5,4 C12.9,4 16,5.9 17.368,9.224 Q17.467,9.5 17.368,9.775 C16,13.1 12.9,15 9.5,15 C6.1,15 3,13.1 1.632,9.775 Q1.533,9.5 1.632,9.224 M11.875,9.5 A2.375,2.375 0,1 1,7.125,9.5 A2.375,2.375 0,1 1,11.875,9.5" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_muted" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_eye_off.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="19dp" android:height="19dp" android:viewportWidth="19" android:viewportHeight="19">
    <group android:translateX="-313" android:translateY="-518.5">
        <path android:pathData="M321.498 522.518C323.342 522.298 325.207 522.688 326.809 523.628C328.41 524.568 329.661 526.007 330.368 527.724C330.434 527.902 330.434 528.097 330.368 528.275C330.077 528.98 329.693 529.643 329.225 530.246M324.15 529.708C323.702 530.141 323.102 530.38 322.48 530.375C321.857 530.37 321.261 530.12 320.821 529.679C320.381 529.239 320.131 528.643 320.125 528.021C320.12 527.398 320.359 526.798 320.792 526.35M326.837 532.353C325.787 532.975 324.616 533.364 323.402 533.494C322.188 533.623 320.961 533.49 319.803 533.103C318.646 532.716 317.585 532.085 316.693 531.252C315.8 530.419 315.098 529.404 314.632 528.275C314.567 528.097 314.567 527.902 314.632 527.724C315.334 526.022 316.569 524.593 318.152 523.652M314.584 520.083L330.417 535.917" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_muted" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_login_unchecked.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="18dp" android:height="18dp" android:viewportWidth="18" android:viewportHeight="18">
    <group android:translateX="-44" android:translateY="-574">
        <path android:pathData="M47.75 576.25H58.25C59.0784 576.25 59.75 576.922 59.75 577.75V588.25C59.75 589.078 59.0784 589.75 58.25 589.75H47.75C46.9216 589.75 46.25 589.078 46.25 588.25V577.75C46.25 576.922 46.9216 576.25 47.75 576.25Z" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_primary" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\login_checkbox.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_checked="true" android:drawable="@drawable/ic_login_checked" />
    <item android:drawable="@drawable/ic_login_unchecked" />
</selector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\login_button_shadow.png`


Действие: использовать готовый PNG из архива по этому же относительному пути.


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\login_card_shadow.png`


Действие: использовать готовый PNG из архива по этому же относительному пути.


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_login.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.core.widget.NestedScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/login_scroll" android:layout_width="match_parent" android:layout_height="match_parent"
    android:fillViewport="true" android:clipToPadding="true" android:scrollbars="none"
    android:paddingTop="86dp" android:paddingBottom="34dp" android:focusableInTouchMode="true" android:descendantFocusability="beforeDescendants">
    <LinearLayout android:id="@+id/login_content" android:focusableInTouchMode="true" android:descendantFocusability="beforeDescendants" android:layout_width="match_parent" android:layout_height="wrap_content"
        android:orientation="vertical" android:paddingStart="4dp" android:paddingEnd="4dp"
        android:clipChildren="false" android:clipToPadding="false">
        <ImageView android:layout_width="56dp" android:layout_height="56dp" android:layout_marginStart="20dp"
            android:background="@drawable/bg_login_brand" android:src="@drawable/ic_login_brand" android:contentDescription="@null" android:importantForAccessibility="no" />
        <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text"
            android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="16dp"
            android:layout_marginStart="20dp" android:layout_marginEnd="20dp" android:layout_marginTop="18dp" android:fontFamily="@font/inter_bold"
            android:text="@string/login_brand" android:textSize="13sp" android:textColor="@color/studyflow_primary" />
        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/login_title" style="@style/StudyFlow.Login.Text"
            android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginStart="20dp" android:layout_marginEnd="20dp"
            android:layout_marginTop="17dp" android:fontFamily="@font/inter_bold" android:text="@string/login_title" android:textSize="34sp" app:lineHeight="39sp" />
        <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text"
            android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginStart="20dp" android:layout_marginEnd="20dp"
            android:layout_marginTop="17dp" android:paddingTop="2dp" android:paddingBottom="2dp" android:lineSpacingExtra="4sp"
            android:text="@string/login_description" android:textSize="14sp" android:textColor="@color/studyflow_muted" />
        <FrameLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="17dp"
            android:layout_marginBottom="-7dp" android:background="@drawable/login_card_shadow" android:clipChildren="false" android:clipToPadding="false">
            <LinearLayout android:id="@+id/login_card" android:layout_width="match_parent" android:layout_height="wrap_content"
                android:layout_marginStart="20dp" android:layout_marginEnd="20dp" android:layout_marginTop="15dp" android:layout_marginBottom="25dp"
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
        <FrameLayout
            android:id="@+id/login_button_container"
            android:layout_width="match_parent"
            android:layout_height="52dp"
            android:layout_marginTop="5dp"
            android:clipChildren="false"
            android:clipToPadding="false">

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
                android:src="@drawable/login_button_shadow"
                android:translationY="8dp" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/login_submit"
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
                android:text="@string/login_submit"
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


            </LinearLayout>
        </FrameLayout>
        <LinearLayout android:layout_width="match_parent" android:layout_height="48dp" android:gravity="center" android:orientation="horizontal" android:layout_marginStart="20dp" android:layout_marginEnd="20dp">
            <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text" android:layout_width="wrap_content" android:layout_height="match_parent" android:gravity="center_vertical" android:text="@string/login_account_prompt" android:textSize="13sp" />
            <androidx.appcompat.widget.AppCompatTextView android:id="@+id/login_create_account" style="@style/StudyFlow.Login.Text" android:layout_width="wrap_content" android:layout_height="match_parent" android:gravity="center_vertical"
                android:fontFamily="@font/inter_semibold" android:text="@string/login_create_account" android:textSize="13sp" android:textColor="@color/studyflow_primary" android:background="?attr/selectableItemBackgroundBorderless" android:clickable="true" android:focusable="true" />
        </LinearLayout>
        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/login_legal" style="@style/StudyFlow.Login.Text" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginStart="20dp" android:layout_marginEnd="20dp"
            android:layout_marginTop="6dp" android:paddingTop="2dp" android:paddingBottom="2dp" android:gravity="center" android:text="@string/login_legal" android:textSize="11sp" app:lineHeight="17sp" android:textColor="@color/studyflow_muted" />
    </LinearLayout>
</androidx.core.widget.NestedScrollView>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\login_strings.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
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
</resources>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\login_styles.xml`


Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
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
</resources>
```


## 5. Проверка

- `assembleDebug` и `lintDebug`: успешно, ошибок 0. Предупреждений 14 — прежние замечания о ресурсах, размерах текста предыдущих экранов и доступной версии Gradle-плагина; новый экран не добавил предупреждений.
- Проверено в Android-эмуляторе API 37: переходы Log In / Skip / Get Started последнего шага и возврат назад.
- Проверены ввод тестового email и пароля, переключатель видимости, чекбокс и отсутствие перехода/авторизации после Log In.
- При 390×844 dp заголовок начинается в x=24, y=193; карточка — x=24, y=364.33; кнопка — x=44, y=612.33. Отличие от целых координат SVG связано с округлением метрик шрифта.
- Проверен небольшой экран 360×640 dp с размером текста 130%: доступна прокрутка, поле пароля полностью находится над клавиатурой.
- Настройки эмулятора восстановлены. Тестовые значения убраны повторным открытием экрана.
- 57 прежних файлов проверены по SHA-256 и не изменены. Runtime-проверка на API 24 отдельно не выполнялась; проект сохраняет minSdk 24.

Ожидаемый результат: белый экран входа как на макете, без автоматически открытой клавиатуры и без курсора в поле при первом открытии. На небольшом экране содержимое можно прокрутить.

Скриншоты: `Login-390x844.png`, `Login-emulator.png`, `Login-small-font130.png`, `Login-small-keyboard.png`. Подробности проверок — `verification.json`.
