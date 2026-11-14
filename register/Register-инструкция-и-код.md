# StudyFlowApp — Register

## 1. Анализ дизайна

Экран реализован по Register.svg размером 390×929: фон #F5F7FC, стрелка назад, Create account, заголовок A fresh start, in flow., описание и белая карточка со скруглением 22 dp. Поля имеют высоту 52 dp. Year и Group расположены в одной строке. Под карточкой — чекбокс, Create Account и ссылка Log In.

По твоей просьбе все шесть полей изначально пустые: Full name, University email, Password, University, Year и Group. Под паролем оставлена согласованная подпись At least 8 characters. Она не является проверкой надёжности пароля.

Иконки email, глаза, стрелки кнопки, фон полей, фон карточки, шрифты Inter и базовые стили переиспользованы из Login/onboarding. Системные часы, значки и нижняя полоса жестов отображаются Android; их оформление зависит от устройства.

## 2. Какие файлы нужны

Экран уже установлен в проект. Вручную вставлять код сейчас не требуется.

Из существующих файлов изменены только LoginActivity.kt (переход по Create an account) и AndroidManifest.xml (регистрация новой Activity). Остальные перечисленные ниже файлы созданы для Register:


- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\AndroidManifest.xml` — изменён.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\LoginActivity.kt` — изменён.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\RegisterActivity.kt` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_register_back.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_back.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_checked.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_chevron.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_person.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_unchecked.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\register_checkbox.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\register_card_shadow.png` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_register.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\register_colors.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\register_strings.xml` — создан.

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\register_styles.xml` — создан.


## 3. Пошаговая инструкция

1. Открой Android Studio и проект `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`.
2. Выбери конфигурацию **app** и эмулятор, нажми зелёную кнопку **Run ▶**.
3. После splash открой **Log In** на onboarding.
4. Внизу Login нажми **Create an account**. Откроется новая регистрация.
5. Проверь, что все поля пустые. В Full name, University email и Password можно вводить текст. Значок глаза показывает и скрывает введённый пароль.
6. Чекбокс согласия переключается. Его начальное состояние отмечено, как на макете. Create Account пока закрывает клавиатуру и остаётся на экране — аккаунт не создаётся.
7. University, Year и Group пока воспроизводят внешний вид выбора со стрелками и реакцией на нажатие. Списки вариантов и логика выбора не добавлены, поскольку их содержимое и макеты ещё не заданы.
8. Стрелка сверху, системная кнопка «Назад» и нижняя ссылка **Log In** возвращают на Login. При открытой клавиатуре системная кнопка «Назад» сначала закрывает её.

Текст Terms of Service и Privacy Policy пока только оформлен цветом, как в макете; страницы документов и их адреса не заданы. База данных, регистрация, запросы, сохранение профиля и проверка пароля не добавлялись.

Для переноса в копию этого же проекта распакуй StudyFlowApp-register.zip и скопируй его папку app в корень проекта, объединив папки. Архив содержит только файлы этого этапа и требует существующие ресурсы Login/onboarding. Резервные копии двух изменённых файлов находятся в папке backup рядом с этой инструкцией.

## 4. Готовый код

Ниже полный код каждого текстового файла.

Для нового Kotlin-файла: в Android Studio открой основную группу kotlin+java → com.example.studyflowapp (без test/androidTest), нажми правой кнопкой → New → Kotlin Class/File → File, имя RegisterActivity. Замени содержимое кодом ниже.

Для XML-разметки: res → layout → New → Layout Resource File, имя activity_register. Открой вкладку Code и вставь код целиком.

Для остальных XML: в соответствующей папке res/drawable или res/values выбери New → Drawable Resource File / Values Resource File, введи имя из указанного пути без .xml, затем полностью вставь код.

Для существующих LoginActivity.kt и AndroidManifest.xml: открой именно указанный файл, выдели старый код целиком и замени соответствующим кодом ниже. Эти версии сохраняют код предыдущих экранов.

PNG тени не нужно создавать вручную: скопируй готовый register_card_shadow.png из архива в app/src/main/res/drawable-xxhdpi. Эта папка уже есть в проекте.


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\AndroidManifest.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


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
        <activity
            android:name=".RegisterActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Register"
            android:windowSoftInputMode="adjustResize|stateAlwaysHidden" />
    </application>

</manifest>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\LoginActivity.kt`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```kotlin
package com.example.studyflowapp

import android.content.Intent
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
    private var openingRegistration = false
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

        findViewById<View>(R.id.login_create_account).setOnClickListener {
            if (!openingRegistration) {
                openingRegistration = true
                startActivity(Intent(this, RegisterActivity::class.java))
            }
        }

        val password = findViewById<EditText>(R.id.login_password)
        val email = findViewById<EditText>(R.id.login_email)
        for (field in listOf(email, password)) {
            field.setOnClickListener {
                field.requestFocus()
                WindowInsetsControllerCompat(window, field).show(WindowInsetsCompat.Type.ime())
            }
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

    override fun onResume() {
        super.onResume()
        openingRegistration = false
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\RegisterActivity.kt`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```kotlin
package com.example.studyflowapp

import android.graphics.Color
import android.graphics.Rect
import android.view.TouchDelegate
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

class RegisterActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.rgb(23, 36, 67))
        )
        setContentView(R.layout.activity_register)
        val scroll = findViewById<NestedScrollView>(R.id.register_scroll)
        findViewById<View>(R.id.register_content).requestFocus()
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
                top = maxOf(bars.top, cutout.top, dp(44)) + dp(16),
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

        findViewById<View>(R.id.register_back).setOnClickListener { finish() }
        findViewById<View>(R.id.register_login).setOnClickListener { finish() }
        val memberRow = findViewById<View>(R.id.register_member_row)
        val loginLink = findViewById<View>(R.id.register_login)
        memberRow.post {
            val area = Rect()
            loginLink.getHitRect(area)
            area.inset(-dp(12), 0)
            memberRow.touchDelegate = TouchDelegate(area, loginLink)
        }
        val headerRow = findViewById<View>(R.id.register_header_row)
        val back = findViewById<View>(R.id.register_back)
        headerRow.post {
            val area = Rect()
            back.getHitRect(area)
            area.inset(-dp(2), -dp(2))
            headerRow.touchDelegate = TouchDelegate(area, back)
        }

        val password = findViewById<EditText>(R.id.register_password)
        val email = findViewById<EditText>(R.id.register_email)
        for (field in listOf(findViewById<EditText>(R.id.register_name), email, password)) {
            field.setOnClickListener {
                field.requestFocus()
                WindowInsetsControllerCompat(window, field).show(WindowInsetsCompat.Type.ime())
            }
            field.setOnFocusChangeListener { _, focused ->
                if (focused && previousImeBottom > 0) revealFocusedField()
            }
        }
        val toggle = findViewById<ImageButton>(R.id.register_password_toggle)
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
            findViewById<View>(R.id.register_content).requestFocus()
        }
        // UI preview only: no credential validation, storage or network requests.
        findViewById<View>(R.id.register_submit).setOnClickListener { closeKeyboard() }
        password.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) { closeKeyboard(); true } else false
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_register_back.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<ripple xmlns:android="http://schemas.android.com/apk/res/android" android:color="#164564ED">
    <item><shape><solid android:color="@color/studyflow_white" /><corners android:radius="14dp" /></shape></item>
</ripple>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_back.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="22dp" android:height="22dp" android:viewportWidth="22" android:viewportHeight="22">
    <group android:translateX="-35" android:translateY="-71">
        <path android:pathData="M46.0004 75.5825L39.583 81.9999L46.0004 88.4173M39.583 81.9999H52.4178" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_ink" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_checked.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="20dp" android:height="20dp" android:viewportWidth="20" android:viewportHeight="20">
    <group android:translateX="-24" android:translateY="-747">
        <path android:pathData="M31.5 757L33.1667 758.667L36.5 755.333M28.1667 749.5H39.8333C40.7538 749.5 41.5 750.246 41.5 751.167V762.833C41.5 763.754 40.7538 764.5 39.8333 764.5H28.1667C27.2462 764.5 26.5 763.754 26.5 762.833V751.167C26.5 750.246 27.2462 749.5 28.1667 749.5Z" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_primary" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_chevron.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="19dp" android:height="19dp" android:viewportWidth="19" android:viewportHeight="19">
    <group android:translateX="-313" android:translateY="-580.5">
        <path android:pathData="M317.75 587.625L322.5 592.375L327.25 587.625" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_muted" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_person.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="19dp" android:height="19dp" android:viewportWidth="19" android:viewportHeight="19">
    <group android:translateX="-313" android:translateY="-288.5">
        <path android:pathData="M322.5 298.792C324.686 298.792 326.458 297.019 326.458 294.833C326.458 292.647 324.686 290.875 322.5 290.875C320.314 290.875 318.542 292.647 318.542 294.833C318.542 297.019 320.314 298.792 322.5 298.792ZM322.5 298.792C324.179 298.792 325.79 299.459 326.978 300.647C328.165 301.834 328.832 303.445 328.832 305.125M322.5 298.792C320.82 298.792 319.209 299.459 318.022 300.647C316.834 301.834 316.167 303.445 316.167 305.125" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_muted" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_register_unchecked.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="20dp" android:height="20dp" android:viewportWidth="20" android:viewportHeight="20">
    <group android:translateX="-24" android:translateY="-747">
        <path android:pathData="M28.1667 749.5H39.8333C40.7538 749.5 41.5 750.246 41.5 751.167V762.833C41.5 763.754 40.7538 764.5 39.8333 764.5H28.1667C27.2462 764.5 26.5 763.754 26.5 762.833V751.167C26.5 750.246 27.2462 749.5 28.1667 749.5Z" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_primary" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\register_checkbox.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_checked="true" android:drawable="@drawable/ic_register_checked" />
    <item android:drawable="@drawable/ic_register_unchecked" />
</selector>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\register_card_shadow.png`


Действие: скопировать готовый PNG из архива по этому же относительному пути.


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_register.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.core.widget.NestedScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/register_scroll" android:layout_width="match_parent" android:layout_height="match_parent"
    android:fillViewport="true" android:clipToPadding="true" android:scrollbars="none" android:paddingTop="60dp" android:paddingBottom="34dp">
    <LinearLayout android:id="@+id/register_content" android:layout_width="match_parent" android:layout_height="wrap_content"
        android:orientation="vertical" android:paddingStart="4dp" android:paddingEnd="4dp"
        android:clipChildren="false" android:clipToPadding="false" android:focusableInTouchMode="true" android:descendantFocusability="beforeDescendants">
        <LinearLayout android:id="@+id/register_header_row" android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="44dp"
            android:layout_marginStart="20dp" android:layout_marginEnd="20dp" android:orientation="horizontal" android:gravity="center_vertical">
            <androidx.appcompat.widget.AppCompatImageButton android:id="@+id/register_back" android:layout_width="44dp" android:layout_height="44dp"
                android:padding="11dp" android:src="@drawable/ic_register_back" android:background="@drawable/bg_register_back" android:contentDescription="@string/register_back" />
            <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text" android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1"
                android:layout_marginStart="12dp" android:fontFamily="@font/inter_bold" android:textSize="22sp" android:text="@string/register_header" />
        </LinearLayout>
        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/register_title" style="@style/StudyFlow.Login.Text"
            android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginStart="20dp" android:layout_marginEnd="20dp" android:layout_marginTop="20dp"
            android:fontFamily="@font/inter_bold" android:textSize="29sp" android:text="@string/register_title" />
        <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text" android:layout_width="match_parent" android:layout_height="wrap_content"
            android:layout_marginStart="20dp" android:layout_marginEnd="20dp" android:layout_marginTop="8dp" android:paddingTop="2dp" android:paddingBottom="2dp"
            android:text="@string/register_description" android:textSize="14sp" android:lineSpacingExtra="4sp" android:textColor="@color/studyflow_muted" />
        <FrameLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="5dp" android:layout_marginBottom="-19dp"
            android:background="@drawable/register_card_shadow" android:clipChildren="false" android:clipToPadding="false">
            <LinearLayout android:id="@+id/register_card" android:layout_width="match_parent" android:layout_height="wrap_content"
                android:layout_marginStart="20dp" android:layout_marginEnd="20dp" android:layout_marginTop="15dp" android:layout_marginBottom="25dp"
                android:padding="20dp" android:orientation="vertical" android:background="@drawable/bg_login_card">
<androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label"
        android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="0dp"
        android:text="@string/register_name_label" android:labelFor="@id/register_name" /><FrameLayout android:layout_width="match_parent" android:layout_height="52dp" android:layout_marginTop="8dp"
        android:background="@drawable/bg_login_field" android:addStatesFromChildren="true">
        <androidx.appcompat.widget.AppCompatEditText android:id="@+id/register_name" style="@style/StudyFlow.Login.Input"
            android:layout_width="match_parent" android:layout_height="match_parent" android:inputType="textPersonName"
            android:imeOptions="actionNext" android:autofillHints="personName" android:nextFocusForward="@id/register_email" />
        <ImageView android:layout_width="19dp" android:layout_height="19dp" android:layout_gravity="end|center_vertical"
        android:layout_marginEnd="14dp" android:src="@drawable/ic_register_person" android:contentDescription="@null" android:importantForAccessibility="no" />
    </FrameLayout><androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label"
        android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="16dp"
        android:text="@string/register_email_label" android:labelFor="@id/register_email" /><FrameLayout android:layout_width="match_parent" android:layout_height="52dp" android:layout_marginTop="8dp"
        android:background="@drawable/bg_login_field" android:addStatesFromChildren="true">
        <androidx.appcompat.widget.AppCompatEditText android:id="@+id/register_email" style="@style/StudyFlow.Login.Input"
            android:layout_width="match_parent" android:layout_height="match_parent" android:inputType="textEmailAddress"
            android:imeOptions="actionNext" android:autofillHints="emailAddress" android:nextFocusForward="@id/register_password" />
        <ImageView android:layout_width="19dp" android:layout_height="19dp" android:layout_gravity="end|center_vertical"
        android:layout_marginEnd="14dp" android:src="@drawable/ic_login_email" android:contentDescription="@null" android:importantForAccessibility="no" />
    </FrameLayout><androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label"
        android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="16dp"
        android:text="@string/register_password_label" android:labelFor="@id/register_password" /><FrameLayout android:layout_width="match_parent" android:layout_height="52dp" android:layout_marginTop="8dp"
        android:background="@drawable/bg_login_field" android:addStatesFromChildren="true">
        <androidx.appcompat.widget.AppCompatEditText android:id="@+id/register_password" style="@style/StudyFlow.Login.Input"
            android:layout_width="match_parent" android:layout_height="match_parent" android:inputType="textPassword"
            android:imeOptions="actionDone" android:autofillHints="newPassword" android:saveEnabled="false" />
        <androidx.appcompat.widget.AppCompatImageButton android:id="@+id/register_password_toggle" android:layout_width="48dp" android:layout_height="match_parent" android:layout_gravity="end"
        android:background="?attr/selectableItemBackgroundBorderless" android:padding="0dp" android:scaleType="center" android:src="@drawable/ic_login_eye_off" android:contentDescription="@string/login_show_password" />
    </FrameLayout>
                <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text" android:layout_width="match_parent" android:layout_height="wrap_content"
                    android:layout_marginTop="7dp" android:text="@string/register_password_helper" android:textSize="10sp" android:textColor="@color/studyflow_register_helper" />
<androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label"
        android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="16dp"
        android:text="@string/register_university_label" android:labelFor="@id/register_university" /><androidx.appcompat.widget.AppCompatTextView android:id="@+id/register_university" style="@style/StudyFlow.Login.Text"
        android:layout_width="match_parent" android:layout_height="52dp" android:layout_marginTop="8dp"
        android:background="@drawable/bg_login_field" android:foreground="?attr/selectableItemBackground"
        android:paddingStart="14dp" android:paddingEnd="14dp" android:gravity="center_vertical" android:textSize="14sp"
        android:drawableEnd="@drawable/ic_register_chevron" android:contentDescription="@string/register_university_label"
        android:clickable="true" android:focusable="true" />
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="16dp" android:orientation="horizontal" android:baselineAligned="false">
                    <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:layout_marginEnd="6dp" android:orientation="vertical">
<androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label"
        android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="0dp"
        android:text="@string/register_year_label" android:labelFor="@id/register_year" /><androidx.appcompat.widget.AppCompatTextView android:id="@+id/register_year" style="@style/StudyFlow.Login.Text"
        android:layout_width="match_parent" android:layout_height="52dp" android:layout_marginTop="8dp"
        android:background="@drawable/bg_login_field" android:foreground="?attr/selectableItemBackground"
        android:paddingStart="14dp" android:paddingEnd="14dp" android:gravity="center_vertical" android:textSize="14sp"
        android:drawableEnd="@drawable/ic_register_chevron" android:contentDescription="@string/register_year_label"
        android:clickable="true" android:focusable="true" />
                    </LinearLayout>
                    <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:layout_marginStart="6dp" android:orientation="vertical">
<androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label"
        android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="0dp"
        android:text="@string/register_group_label" android:labelFor="@id/register_group" /><androidx.appcompat.widget.AppCompatTextView android:id="@+id/register_group" style="@style/StudyFlow.Login.Text"
        android:layout_width="match_parent" android:layout_height="52dp" android:layout_marginTop="8dp"
        android:background="@drawable/bg_login_field" android:foreground="?attr/selectableItemBackground"
        android:paddingStart="14dp" android:paddingEnd="14dp" android:gravity="center_vertical" android:textSize="14sp"
        android:drawableEnd="@drawable/ic_register_chevron" android:contentDescription="@string/register_group_label"
        android:clickable="true" android:focusable="true" />
                    </LinearLayout>
                </LinearLayout>
            </LinearLayout>
        </FrameLayout>
        <androidx.appcompat.widget.AppCompatCheckBox android:id="@+id/register_agreement" style="@style/StudyFlow.Login.Text" android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="48dp"
            android:layout_marginStart="20dp" android:layout_marginEnd="20dp" android:button="@null" app:buttonCompat="@null" android:drawableStart="@drawable/register_checkbox" android:drawablePadding="9dp"
            android:padding="0dp" android:checked="true" android:background="?attr/selectableItemBackgroundBorderless" android:gravity="center_vertical"
            android:text="@string/register_agreement" android:textSize="11sp" android:textColor="@color/studyflow_muted" />
        <FrameLayout
            android:id="@+id/register_button_container"
            android:layout_width="match_parent"
            android:layout_height="52dp"
            android:layout_marginTop="6dp"
            android:layout_marginStart="20dp" android:layout_marginEnd="20dp"
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
                android:src="@drawable/onboarding_button_shadow"
                android:translationY="8dp" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/register_submit"
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
                android:text="@string/register_submit"
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
        <LinearLayout android:id="@+id/register_member_row" android:layout_width="match_parent" android:layout_height="48dp" android:layout_marginTop="5dp"
            android:layout_marginStart="20dp" android:layout_marginEnd="20dp" android:gravity="center" android:orientation="horizontal">
            <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text" android:layout_width="wrap_content" android:layout_height="match_parent"
                android:gravity="center_vertical" android:text="@string/register_member" android:textSize="12sp" android:textColor="@color/studyflow_muted" />
            <androidx.appcompat.widget.AppCompatTextView android:id="@+id/register_login" style="@style/StudyFlow.Login.Text" android:layout_width="wrap_content" android:layout_height="match_parent"
                android:gravity="center_vertical" android:fontFamily="@font/inter_semibold" android:text="@string/login_submit" android:textSize="12sp" android:textColor="@color/studyflow_primary"
                android:background="?attr/selectableItemBackgroundBorderless" android:clickable="true" android:focusable="true" />
        </LinearLayout>
    </LinearLayout>
</androidx.core.widget.NestedScrollView>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\register_colors.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="studyflow_register_background">#F5F7FC</color>
    <color name="studyflow_register_helper">#23816B</color>
</resources>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\register_strings.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="register_back">Back to login</string>
    <string name="register_header">Create account</string>
    <string name="register_title">A fresh start, in flow.</string>
    <string name="register_description">Set up your academic profile. We’ll help you make\nthe most of every week.</string>
    <string name="register_name_label">Full name</string>
    <string name="register_email_label">University email</string>
    <string name="register_password_label">Password</string>
    <string name="register_password_helper">At least 8 characters</string>
    <string name="register_university_label">University</string>
    <string name="register_year_label">Year</string>
    <string name="register_group_label">Group</string>
    <string name="register_agreement">I agree to the <font color="#4564ED">Terms of Service</font> and <font color="#4564ED">Privacy Policy</font>.</string>
    <string name="register_submit">Create Account</string>
    <string name="register_member">"Already a member? "</string>
</resources>
```


### Файл: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\register_styles.xml`


Действие: создать файл, если его нет, или полностью заменить содержимое следующим кодом.


```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.StudyFlowApp.Register" parent="Theme.StudyFlowApp.Onboarding">
        <item name="android:windowBackground">@color/studyflow_register_background</item>
    </style>
</resources>
```


## 5. Проверка

- assembleDebug и lintDebug: успешно, ошибок 0. Lint отмечает подпись 10 sp под паролем как SmallSp; размер взят из макета. Остальные предупреждения существовали до этого этапа.
- Эмулятор API 37: подтверждены шесть пустых полей, отсутствие автоматического фокуса при открытии, ввод имени/email/пароля, показ и скрытие пароля, переключение чекбокса.
- Проверены открытие Register из Login, возврат по верхней стрелке и нижнему Log In, повторное открытие, отсутствие реальной регистрации по Create Account.
- Снято сравнение при 390×929 dp и проверен экран 360×640 dp с текстом 130%. На небольшом экране форма прокручивается, кнопки доступны, клавиатура не перекрывает активное поле после прокрутки.
- 73 прежних файлов проверены по SHA-256 и не изменены. Настройки размера экрана, плотности и шрифта эмулятора восстановлены. Настройки клавиатуры Gboard не менялись.
- Сохранён minSdk 24; отдельный запуск на Android 7/API 24 не выполнялся.

Скриншоты: Register-390x929.png, Register-emulator.png, Register-small-font130.png, Register-small-keyboard.png. Результаты проверок: verification.json.
