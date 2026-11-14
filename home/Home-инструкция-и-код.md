# Home dashboard — главный экран StudyFlow

Экран уже добавлен в `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`. Вручную переносить код сейчас не нужно. Ниже сохранены инструкция и полные версии файлов.

## 1. Анализ дизайна

На экране: дата и приветствие, уведомления, градиентная карточка недельного прогресса с кольцом 75%, ближайший дедлайн, две карточки приоритетов, сегодняшнее занятие и следующее занятие, кнопка «+», нижняя панель Home / Schedule / Tasks / Notes / Profile.

Иконки перенесены из SVG в Vector Drawable; используются существующие шрифты Inter. Фон — #F5F7FC. Вертикальный градиент — #273D86 → #4969E8 (55%) → #9672D6. Карточки и отступы соответствуют макету 390 × 1008. Строка состояния и панель жестов принадлежат Android; их значки и размеры отличаются от iOS-макета.

Содержимое прокручивается на небольшом экране. Нижняя навигация и кнопка «+» закреплены. Текстовые блоки могут увеличиваться при увеличении системного шрифта.

## 2. Какие файлы нужны

Созданы HomeActivity.kt, activity_home.xml, home_strings.xml, home_styles.xml, XML-фоны, векторные иконки и два PNG-ресурса теней. Из существующих файлов изменены только AndroidManifest.xml, LoginActivity.kt и RegisterActivity.kt. Остальные экраны и ресурсы сохранены. Предыдущие версии трёх изменённых файлов находятся в папке `backup` рядом с инструкцией.

## 3. Пошаговая инструкция

1. В Android Studio открой **File → Open** и выбери `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`, если этот проект ещё не открыт.
2. Дождись завершения синхронизации Gradle.
3. Выбери конфигурацию **app** и эмулятор или подключённый телефон.
4. Нажми зелёную кнопку **Run ▶**.
5. Перейди с onboarding на **Log In**. Введи любой тестовый email и пароль минимум из 8 символов. Нажми **Log In** — откроется Home.
6. Второй путь: **Create an account**, заполни имя, email, пароль и университет, установи галочку согласия. Нажми **Create Account** — откроется тот же Home.

Пока это демонстрационный переход после локальной проверки полей, без создания аккаунта и обращения к серверу. Имя Aruzhan, дата, задачи и проценты взяты из макета и пока не меняются по введённым данным. Галочки задач можно переключать для проверки внешнего вида; они не сохраняются в базе и не пересчитывают прогресс. Уведомления, «+», See all, 4 classes и остальные вкладки пока показывают только реакцию на нажатие. Системная кнопка «Назад» возвращает к форме.

## 4. Готовый код

Полный код приведён ниже с абсолютными путями. Если потребуется перенести изменения вручную, используй архив StudyFlowApp-home.zip: внутри сохранены пути относительно корня проекта. Он содержит только файлы этого этапа.

Для нового Kotlin-файла: в пакете `com.example.studyflowapp` нажми правой кнопкой → **New → Kotlin Class/File → File**, введи **HomeActivity** и вставь код. Для нового XML-файла в указанной папке `res` выбери **New → Android Resource File**, задай имя без `.xml` и тип **Layout**, **Drawable** или **Values**, соответствующий папке. В каждом файле полностью замени содержимое кодом из инструкции. PNG-файлы скопируй из архива в `res/drawable-xxhdpi`; их нельзя вставлять как XML.

Папка `values-v28` содержит настройку высоты строки для Android 9 и новее. При ручном переносе создай её через **res → New → Android Resource Directory → Resource type: values → Version → API level: 28**. Базовый файл в `values` нужен тоже: он обеспечивает совместимость с Android 7–8. Папку `drawable-xxhdpi` при необходимости создай через тот же пункт, выбрав **Drawable → Density → XX-High Density**. При копировании архива эти папки уже подготовлены.


### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\AndroidManifest.xml`

Действие: заменить содержимое существующего файла.

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
        <activity
            android:name=".HomeActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Home" />
    </application>

</manifest>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\HomeActivity.kt`

Действие: создать файл по указанному пути.

```kotlin
package com.example.studyflowapp

import android.graphics.Color
import android.graphics.Rect
import android.os.Bundle
import android.view.TouchDelegate
import android.view.View
import android.view.ViewGroup
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updateLayoutParams
import androidx.core.view.updatePadding

/** Figma preview data only. Tasks, notifications and other tabs are not connected yet. */
class HomeActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.rgb(23, 36, 67))
        )
        setContentView(R.layout.activity_home)
        val root = findViewById<View>(R.id.home_root)
        val scroll = findViewById<View>(R.id.home_scroll)
        val navigation = findViewById<View>(R.id.home_navigation)
        val add = findViewById<View>(R.id.home_add_container)
        ViewCompat.setOnApplyWindowInsetsListener(root) { _, insets ->
            val safe = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout())
            scroll.updatePadding(left = safe.left, top = maxOf(safe.top, dp(44)) + dp(16), right = safe.right)
            navigation.updatePadding(left = safe.left, right = safe.right, bottom = maxOf(safe.bottom, dp(34)))
            add.updateLayoutParams<ViewGroup.MarginLayoutParams> { marginEnd = dp(24) + safe.right }
            insets
        }
        ViewCompat.requestApplyInsets(root)
        findViewById<View>(R.id.home_tab_home).isSelected = true
        // Enlarge small visual controls without changing the Figma layout.
        for (id in listOf(R.id.home_check_problem, R.id.home_check_diagram,
                R.id.home_notifications, R.id.home_see_all, R.id.home_class_count)) {
            val target = findViewById<View>(id)
            val parent = target.parent as View
            parent.post {
                val rect = Rect()
                target.getHitRect(rect)
                rect.inset(-maxOf(0, (dp(48) - rect.width()) / 2), -maxOf(0, (dp(48) - rect.height()) / 2))
                parent.touchDelegate = TouchDelegate(rect, target)
            }
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\LoginActivity.kt`

Действие: заменить содержимое существующего файла.

```kotlin
package com.example.studyflowapp

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.text.method.HideReturnsTransformationMethod
import android.text.method.PasswordTransformationMethod
import android.view.View
import android.view.ViewGroup
import androidx.core.widget.doAfterTextChanged
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
    private var openingHome = false
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
        val passwordError = findViewById<View>(R.id.login_password_error)
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
            field.doAfterTextChanged { updateFormState() }
            field.setOnClickListener {
                field.requestFocus()
                WindowInsetsControllerCompat(window, field).show(WindowInsetsCompat.Type.ime())
            }
            field.setOnFocusChangeListener { _, focused ->
                if (focused && previousImeBottom > 0) revealFocusedField()
            }
        }
        updateFormState()
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
        // Local form feedback only; account verification is not connected.
        submit.setOnClickListener {
            if (formIsValid() && !openingHome) {
                openingHome = true
                closeKeyboard()
                startActivity(Intent(this, HomeActivity::class.java))
            }
        }
        password.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) { closeKeyboard(); true } else false
        }
    }

    override fun onResume() {
        super.onResume()
        openingHome = false
        openingRegistration = false
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\RegisterActivity.kt`

Действие: заменить содержимое существующего файла.

```kotlin
package com.example.studyflowapp

import android.content.Intent
import android.graphics.Color
import android.graphics.Rect
import android.view.TouchDelegate
import android.os.Bundle
import android.text.method.HideReturnsTransformationMethod
import android.text.method.PasswordTransformationMethod
import android.view.View
import android.view.ViewGroup
import android.view.inputmethod.EditorInfo
import android.widget.CheckBox
import androidx.core.widget.doAfterTextChanged
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
    private var openingHome = false
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

        val name = findViewById<EditText>(R.id.register_name)
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
            field.setOnClickListener {
                field.requestFocus()
                WindowInsetsControllerCompat(window, field).show(WindowInsetsCompat.Type.ime())
            }
            field.setOnFocusChangeListener { _, focused ->
                if (focused && previousImeBottom > 0) revealFocusedField()
            }
        }
        updateFormState()
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
        // UI feedback only: no account creation, storage or network requests.
        submit.setOnClickListener {
            if (formIsValid() && !openingHome) {
                openingHome = true
                closeKeyboard()
                startActivity(Intent(this, HomeActivity::class.java))
            }
        }
        university.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) { closeKeyboard(); true } else false
        }
    }

    override fun onResume() {
        super.onResume()
        openingHome = false
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_bell.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ripple xmlns:android="http://schemas.android.com/apk/res/android" android:color="#164564ED">
    <item>
        <shape>
            <solid android:color="@color/studyflow_white" />
            <corners android:radius="14dp" />
        </shape>
    </item>
</ripple>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_checkbox.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_checked="true" android:drawable="@drawable/ic_home_checked" />
    <item>
        <shape>
            <solid android:color="@color/studyflow_white" />
            <corners android:radius="8dp" />
            <stroke android:width="1.5dp" android:color="#C7D1E3" />
        </shape>
    </item>
</selector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_class.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/studyflow_badge_background" />
    <corners android:radius="18dp" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_deadline.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#F2EDFC" />
    <corners android:radius="22dp" />
    <stroke android:width="1dp" android:color="#E6DDF6" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_divider.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/studyflow_primary" />
    <corners android:radius="2dp" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_dot.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/studyflow_primary" />
    <corners android:radius="3dp" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_hero.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <corners android:radius="22dp" />
    <gradient android:angle="270" android:startColor="#273D86" android:centerColor="#4969E8" android:endColor="#9672D6" android:centerY="0.55" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_high.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FCEEF0" />
    <corners android:radius="11dp" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_hourglass.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#E4D9F8" />
    <corners android:radius="12dp" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_medium.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FFF5E4" />
    <corners android:radius="11dp" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_plus.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ripple xmlns:android="http://schemas.android.com/apk/res/android" android:color="#164564ED">
    <item>
        <shape>
            <solid android:color="@color/studyflow_primary" />
            <corners android:radius="18dp" />
        </shape>
    </item>
</ripple>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_selected.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/studyflow_badge_background" />
    <corners android:radius="14dp" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\bg_home_stats.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#16FFFFFF" />
    <corners android:radius="14dp" />
    <stroke android:width="1dp" android:color="#29FFFFFF" />
</shape>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_bell.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="22dp" android:height="22dp" android:viewportWidth="22" android:viewportHeight="22">
    <group android:translateX="-333" android:translateY="-83">
        <path android:pathData="M342.411 102.251C342.572 102.529 342.804 102.761 343.082 102.922C343.361 103.083 343.677 103.167 343.999 103.167C344.321 103.167 344.637 103.083 344.916 102.922C345.194 102.761 345.426 102.529 345.587 102.251M335.99 97.0491C335.87 97.1803 335.791 97.3435 335.762 97.5189C335.733 97.6943 335.756 97.8742 335.828 98.0367C335.9 98.1993 336.017 98.3376 336.166 98.4347C336.315 98.5318 336.488 98.5836 336.666 98.5837H351.333C351.511 98.5837 351.684 98.5322 351.833 98.4353C351.982 98.3383 352.1 98.2003 352.172 98.0378C352.244 97.8753 352.267 97.6954 352.238 97.5201C352.21 97.3447 352.131 97.1814 352.011 97.05C350.792 95.7931 349.5 94.4574 349.5 90.333C349.5 88.8742 348.92 87.4751 347.889 86.4436C346.857 85.412 345.458 84.8325 344 84.8325C342.541 84.8325 341.142 85.412 340.11 86.4436C339.079 87.4751 338.499 88.8742 338.499 90.333C338.499 94.4574 337.206 95.7931 335.99 97.0491Z" android:fillColor="@android:color/transparent" android:strokeColor="#172443" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_broadcast.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="19dp" android:height="19dp" android:viewportWidth="19" android:viewportHeight="19">
    <group android:translateX="-333" android:translateY="-762.5">
        <path android:pathData="M345.863 768.643C346.752 769.534 347.251 770.741 347.251 771.999C347.251 773.257 346.752 774.464 345.863 775.355M348.102 766.404C349.585 767.889 350.418 769.901 350.418 771.999C350.418 774.097 349.585 776.109 348.102 777.593M336.899 777.593C335.416 776.109 334.583 774.097 334.583 771.999C334.583 769.901 335.416 767.889 336.899 766.404M339.138 775.355C338.249 774.464 337.749 773.257 337.749 771.999C337.749 770.741 338.249 769.534 339.138 768.643M344.084 771.999C344.084 772.874 343.375 773.582 342.5 773.582C341.626 773.582 340.917 772.874 340.917 771.999C340.917 771.125 341.626 770.416 342.5 770.416C343.375 770.416 344.084 771.125 344.084 771.999Z" android:fillColor="@android:color/transparent" android:strokeColor="#4564ED" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_checked.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="@color/studyflow_primary" android:pathData="M8,0 H16 Q24,0 24,8 V16 Q24,24 16,24 H8 Q0,24 0,16 V8 Q0,0 8,0 Z" />
    <path android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_white" android:strokeWidth="1.5" android:strokeLineCap="round" android:strokeLineJoin="round" android:pathData="M6,12 L10,16 L18,8" />
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_home.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="21dp" android:height="21dp" android:viewportWidth="21" android:viewportHeight="21">
    <group android:translateX="-36.5" android:translateY="-931.5">
        <path android:pathData="M49.625 949.875V942.875C49.625 942.642 49.5328 942.42 49.3687 942.256C49.2046 942.092 48.9821 942 48.75 942H45.25C45.0179 942 44.7954 942.092 44.6313 942.256C44.4672 942.42 44.375 942.642 44.375 942.875V949.875M39.125 940.25C39.1249 939.995 39.1804 939.744 39.2876 939.513C39.3947 939.282 39.5509 939.077 39.7454 938.913L45.8704 933.663C46.1862 933.396 46.5864 933.25 47 933.25C47.4136 933.25 47.8138 933.396 48.1296 933.663L54.2546 938.913C54.4491 939.077 54.6053 939.282 54.7124 939.513C54.8196 939.744 54.8751 939.995 54.875 940.25V948.125C54.875 948.589 54.6906 949.034 54.3624 949.362C54.0342 949.691 53.5891 949.875 53.125 949.875H40.875C40.4109 949.875 39.9658 949.691 39.6376 949.362C39.3094 949.034 39.125 948.589 39.125 948.125V940.25Z" android:fillColor="@android:color/transparent" android:strokeColor="#4564ED" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_hourglass.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="22dp" android:height="22dp" android:viewportWidth="22" android:viewportHeight="22">
    <group android:translateX="-49" android:translateY="-373">
        <path android:pathData="M53.583 393.167H55.4166M55.4166 393.167H64.5843M55.4166 393.167V389.343C55.4167 388.856 55.6099 388.39 55.9538 388.046L60.0004 384M64.5843 393.167H66.4178M64.5843 393.167V389.343C64.5842 388.856 64.3909 388.39 64.047 388.046L60.0004 384M53.583 374.833H55.4166M55.4166 374.833H64.5843M55.4166 374.833V378.657C55.4167 379.143 55.6099 379.61 55.9538 379.953L60.0004 384M64.5843 374.833H66.4178M64.5843 374.833V378.657C64.5842 379.143 64.3909 379.61 64.047 379.953L60.0004 384" android:fillColor="@android:color/transparent" android:strokeColor="#8060CC" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_notes.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="21dp" android:height="21dp" android:viewportWidth="21" android:viewportHeight="21">
    <group android:translateX="-258.5" android:translateY="-931.5">
        <path android:pathData="M270.225 933.25H263.749C263.285 933.25 262.84 933.434 262.512 933.762C262.184 934.09 261.999 934.535 261.999 935V936.75M261.999 936.75V940.25M261.999 936.75H260.249M261.999 936.75H263.749M261.999 940.25V943.75M261.999 940.25H260.249M261.999 940.25H263.749M261.999 943.75V947.251M261.999 943.75H260.249M261.999 943.75H263.749M261.999 947.251V949.001C261.999 949.465 262.184 949.91 262.512 950.238C262.84 950.567 263.285 950.751 263.749 950.751H274.25C274.714 950.751 275.159 950.567 275.488 950.238C275.816 949.91 276 949.465 276 949.001V942.525M261.999 947.251H260.249M261.999 947.251H263.749M277.206 936.423C277.555 936.074 277.75 935.601 277.75 935.108C277.75 934.615 277.555 934.143 277.206 933.794C276.857 933.445 276.385 933.25 275.892 933.25C275.399 933.25 274.926 933.445 274.577 933.794L270.193 938.18C269.985 938.388 269.833 938.645 269.75 938.927L269.018 941.439C268.996 941.514 268.995 941.594 269.014 941.67C269.034 941.746 269.073 941.815 269.129 941.87C269.184 941.926 269.253 941.965 269.329 941.985C269.405 942.004 269.485 942.003 269.561 941.981L272.072 941.249C272.354 941.166 272.611 941.014 272.819 940.806L277.206 936.423Z" android:fillColor="@android:color/transparent" android:strokeColor="#66728B" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_plus.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="22dp" android:height="22dp" android:viewportWidth="22" android:viewportHeight="22">
    <group android:translateX="-328" android:translateY="-858">
        <path android:pathData="M331.416 869H339M339 869H346.584M339 869V861.416M339 869V876.584" android:fillColor="@android:color/transparent" android:strokeColor="#FFFFFF" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_profile.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="21dp" android:height="21dp" android:viewportWidth="21" android:viewportHeight="21">
    <group android:translateX="-332.5" android:translateY="-931.5">
        <path android:pathData="M343 942.875C345.416 942.875 347.375 940.916 347.375 938.5C347.375 936.084 345.416 934.125 343 934.125C340.584 934.125 338.626 936.084 338.626 938.5C338.626 940.916 340.584 942.875 343 942.875ZM343 942.875C344.857 942.875 346.637 943.612 347.95 944.925C349.262 946.238 350 948.018 350 949.875M343 942.875C341.144 942.875 339.364 943.612 338.051 944.925C336.738 946.238 336.001 948.018 336.001 949.875" android:fillColor="@android:color/transparent" android:strokeColor="#66728B" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_progress.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="80dp" android:height="80dp" android:viewportWidth="80" android:viewportHeight="80">
    <group android:translateX="-266" android:translateY="-168">
        <path android:pathData="M346 208C346 230.091 328.091 248 306 248C283.909 248 266 230.091 266 208C266 185.909 283.909 168 306 168C328.091 168 346 185.909 346 208ZM272 208C272 226.778 287.222 242 306 242C324.778 242 340 226.778 340 208C340 189.222 324.778 174 306 174C287.222 174 272 189.222 272 208Z" android:fillColor="#FFFFFF" android:fillAlpha="0.133333" />
        <path android:pathData="M306 168C313.911 168 321.645 170.346 328.223 174.741C334.801 179.136 339.928 185.384 342.955 192.693C345.983 200.002 346.775 208.044 345.231 215.804C343.688 223.563 339.878 230.69 334.284 236.284C328.69 241.878 321.563 245.688 313.804 247.231C306.044 248.775 298.002 247.983 290.693 244.955C283.384 241.928 277.136 236.801 272.741 230.223C268.346 223.645 266 215.911 266 208H272C272 214.725 273.994 221.298 277.73 226.889C281.466 232.481 286.776 236.839 292.989 239.412C299.201 241.985 306.038 242.659 312.633 241.347C319.228 240.035 325.287 236.797 330.042 232.042C334.797 227.287 338.035 221.228 339.347 214.633C340.659 208.038 339.985 201.201 337.412 194.989C334.839 188.776 330.481 183.466 324.889 179.73C319.298 175.994 312.725 174 306 174V168Z" android:fillColor="#FFFFFF" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_schedule.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="21dp" android:height="21dp" android:viewportWidth="21" android:viewportHeight="21">
    <group android:translateX="-110.5" android:translateY="-931.5">
        <path android:pathData="M117.5 933.25V935M117.5 935V936.75M117.5 935H114.875C113.909 935 113.125 935.783 113.125 936.75V940.25M117.5 935H124.5M124.5 933.25V935M124.5 935V936.75M124.5 935H127.125C128.091 935 128.875 935.783 128.875 936.75V940.25M113.125 940.25H128.875M113.125 940.25V949.001C113.125 949.967 113.909 950.751 114.875 950.751H127.125C128.091 950.751 128.875 949.967 128.875 949.001V940.25M117.5 943.75H117.509M121 943.75H121.009M124.5 943.75H124.509M117.5 947.251H117.509M121 947.251H121.009M124.5 947.251H124.509" android:fillColor="@android:color/transparent" android:strokeColor="#66728B" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_home_tasks.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="21dp" android:height="21dp" android:viewportWidth="21" android:viewportHeight="21">
    <group android:translateX="-184.5" android:translateY="-931.5">
        <path android:pathData="M192.375 942L194.125 943.75L197.625 940.25M203.75 942C203.75 946.833 199.833 950.751 195 950.751C190.167 950.751 186.249 946.833 186.249 942C186.249 937.167 190.167 933.25 195 933.25C199.833 933.25 203.75 937.167 203.75 942Z" android:fillColor="@android:color/transparent" android:strokeColor="#66728B" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\home_card_shadow.png`

Действие: создать файл по указанному пути.

Скопировать готовое изображение из архива без переименования.

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\home_plus_shadow.png`

Действие: создать файл по указанному пути.

Скопировать готовое изображение из архива без переименования.

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_home.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" android:id="@+id/home_root" android:layout_width="match_parent" android:layout_height="match_parent" android:background="@color/studyflow_register_background" android:clipChildren="false">
    <androidx.core.widget.NestedScrollView android:id="@+id/home_scroll" android:layout_width="0dp" android:layout_height="0dp" android:clipToPadding="true" android:fillViewport="true" android:scrollbars="none" app:layout_constraintTop_toTopOf="parent" app:layout_constraintBottom_toTopOf="@id/home_navigation" app:layout_constraintStart_toStartOf="parent" app:layout_constraintEnd_toEndOf="parent">
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:paddingStart="24dp" android:paddingEnd="24dp" android:paddingBottom="86dp" android:clipChildren="false" android:clipToPadding="false">
            <FrameLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:id="@+id/home_header">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:layout_marginEnd="56dp" android:minHeight="68dp">
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_date" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:minHeight="14dp" android:text="@string/home_date" android:textSize="11sp" android:fontFamily="@font/inter_medium" android:textColor="@color/studyflow_muted" />
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_greeting" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_greeting" android:textSize="25sp" android:fontFamily="@font/inter_bold" android:textColor="@color/studyflow_ink" android:layout_marginTop="4dp" />
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_subtitle" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_subtitle" android:textSize="12sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_muted" android:layout_marginTop="5dp" />
                </LinearLayout>
                <androidx.appcompat.widget.AppCompatImageButton android:id="@+id/home_notifications" android:layout_width="44dp" android:layout_height="44dp" android:layout_gravity="end|top" android:layout_marginTop="12dp" android:src="@drawable/ic_home_bell" android:padding="11dp" android:background="@drawable/bg_home_bell" android:contentDescription="@string/home_notifications" />
                <View android:layout_width="6dp" android:layout_height="6dp" android:layout_gravity="end|top" android:layout_marginEnd="12dp" android:layout_marginTop="22dp" android:background="@drawable/bg_home_dot" android:importantForAccessibility="no" />
            </FrameLayout>
            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:id="@+id/home_hero" android:layout_marginTop="20dp" android:padding="20dp" android:minHeight="175dp" android:background="@drawable/bg_home_hero">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:baselineAligned="false">
                    <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:layout_weight="1" android:paddingTop="7dp" android:layout_marginEnd="12dp">
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_week" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_week" android:textSize="10sp" android:fontFamily="@font/inter_semibold" android:textColor="#CCFFFFFF" />
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_momentum" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_momentum" android:textSize="21sp" android:fontFamily="@font/inter_bold" android:textColor="@color/studyflow_white" android:layout_marginTop="7dp" />
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_hours" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_hours" android:textSize="12sp" android:fontFamily="@font/inter_regular" android:textColor="#DDFFFFFF" android:layout_marginTop="6dp" />
                    </LinearLayout>
                    <FrameLayout android:layout_width="80dp" android:layout_height="80dp" android:contentDescription="@string/home_progress_description" android:importantForAccessibility="yes" android:descendantFocusability="blocksDescendants">
                        <androidx.appcompat.widget.AppCompatImageView android:layout_width="80dp" android:layout_height="80dp" android:src="@drawable/ic_home_progress" android:importantForAccessibility="no" />
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_percent" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_percent" android:textSize="25sp" android:fontFamily="@font/inter_bold" android:textColor="@color/studyflow_white" android:layout_gravity="center" />
                    </FrameLayout>
                </LinearLayout>
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:baselineAligned="false" android:minHeight="37dp" android:gravity="center_vertical" android:paddingStart="12dp" android:paddingEnd="12dp" android:paddingTop="8dp" android:paddingBottom="8dp" android:layout_marginTop="18dp" android:background="@drawable/bg_home_stats">
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_done" style="@style/StudyFlow.Home.Text" android:layout_width="0dp" android:layout_height="wrap_content" android:text="@string/home_done" android:textSize="11sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_white" android:layout_weight="1" />
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_streak" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_streak" android:textSize="11sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_white" />
                </LinearLayout>
            </LinearLayout>
            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:baselineAligned="false" android:id="@+id/home_deadline" android:gravity="center_vertical" android:padding="16dp" android:minHeight="82dp" android:layout_marginTop="20dp" android:background="@drawable/bg_home_deadline">
                <FrameLayout android:layout_width="40dp" android:layout_height="40dp" android:background="@drawable/bg_home_hourglass">
                    <androidx.appcompat.widget.AppCompatImageView android:layout_width="22dp" android:layout_height="22dp" android:src="@drawable/ic_home_hourglass" android:importantForAccessibility="no" android:layout_gravity="center" />
                </FrameLayout>
                <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:layout_weight="1" android:layout_marginStart="12dp" android:layout_marginEnd="8dp">
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_next_deadline" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_next_deadline" android:textSize="10sp" android:fontFamily="@font/inter_semibold" android:textColor="@color/studyflow_muted" />
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_problem" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_problem" android:textSize="13sp" android:fontFamily="@font/inter_semibold" android:textColor="@color/studyflow_ink" android:layout_marginTop="4dp" />
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_due" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_due" android:textSize="10sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_muted" android:layout_marginTop="4dp" />
                </LinearLayout>
                <LinearLayout android:layout_width="wrap_content" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="end">
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_countdown" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_countdown" android:textSize="19sp" android:fontFamily="@font/inter_bold" android:textColor="#8060CC" />
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_remaining" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_remaining" android:textSize="10sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_muted" android:layout_marginTop="5dp" />
                </LinearLayout>
            </LinearLayout>
            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:baselineAligned="false" android:layout_marginTop="20dp" android:gravity="center_vertical">
                <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_priorities" style="@style/StudyFlow.Home.Text" android:layout_width="0dp" android:layout_height="wrap_content" android:text="@string/home_priorities" android:textSize="17sp" android:fontFamily="@font/inter_bold" android:textColor="@color/studyflow_ink" android:layout_weight="1" />
                <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_see_all" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="match_parent" android:text="@string/home_see_all" android:textSize="12sp" android:fontFamily="@font/inter_semibold" android:textColor="@color/studyflow_primary" android:clickable="true" android:focusable="true" android:background="?attr/selectableItemBackground" android:gravity="center_vertical" />
            </LinearLayout>
            <FrameLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:id="@+id/home_task_problem" android:layout_marginTop="12dp" android:clipChildren="false" android:clipToPadding="false">
                <ImageView android:layout_width="match_parent" android:layout_height="match_parent" android:layout_marginStart="-20dp" android:layout_marginEnd="-20dp" android:layout_marginTop="-15dp" android:layout_marginBottom="-25dp" android:src="@drawable/home_card_shadow" android:scaleType="fitXY" android:importantForAccessibility="no" />
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:baselineAligned="false" android:background="@drawable/bg_login_card" android:padding="16dp" android:minHeight="98dp">
                    <androidx.appcompat.widget.AppCompatCheckBox android:id="@+id/home_check_problem" android:layout_width="24dp" android:layout_height="24dp" android:layout_marginEnd="12dp" android:button="@null" android:background="@drawable/bg_home_checkbox" android:padding="0dp" android:minWidth="0dp" android:minHeight="0dp" android:contentDescription="@string/home_check_problem" />
                    <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:layout_weight="1">
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_problem_title" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_problem" android:textSize="14sp" android:fontFamily="@font/inter_semibold" android:textColor="@color/studyflow_ink" />
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_problem_detail" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_problem_detail" android:textSize="11sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_muted" android:layout_marginTop="7dp" />
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_high" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_high" android:textSize="10sp" android:fontFamily="@font/inter_semibold" android:textColor="#B94958" android:layout_marginTop="7dp" android:background="@drawable/bg_home_high" android:paddingStart="9dp" android:paddingEnd="9dp" android:paddingTop="5dp" android:paddingBottom="5dp" android:minHeight="22dp" android:gravity="center" />
                    </LinearLayout>
                </LinearLayout>
            </FrameLayout>
            <FrameLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:id="@+id/home_task_diagram" android:layout_marginTop="12dp" android:clipChildren="false" android:clipToPadding="false">
                <ImageView android:layout_width="match_parent" android:layout_height="match_parent" android:layout_marginStart="-20dp" android:layout_marginEnd="-20dp" android:layout_marginTop="-15dp" android:layout_marginBottom="-25dp" android:src="@drawable/home_card_shadow" android:scaleType="fitXY" android:importantForAccessibility="no" />
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:baselineAligned="false" android:background="@drawable/bg_login_card" android:padding="16dp" android:minHeight="98dp">
                    <androidx.appcompat.widget.AppCompatCheckBox android:id="@+id/home_check_diagram" android:layout_width="24dp" android:layout_height="24dp" android:layout_marginEnd="12dp" android:button="@null" android:background="@drawable/bg_home_checkbox" android:padding="0dp" android:minWidth="0dp" android:minHeight="0dp" android:contentDescription="@string/home_check_diagram" />
                    <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:layout_weight="1">
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_diagram" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_diagram" android:textSize="14sp" android:fontFamily="@font/inter_semibold" android:textColor="@color/studyflow_ink" />
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_diagram_detail" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_diagram_detail" android:textSize="11sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_muted" android:layout_marginTop="7dp" />
                        <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_medium" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_medium" android:textSize="10sp" android:fontFamily="@font/inter_semibold" android:textColor="#996923" android:layout_marginTop="7dp" android:background="@drawable/bg_home_medium" android:paddingStart="9dp" android:paddingEnd="9dp" android:paddingTop="5dp" android:paddingBottom="5dp" android:minHeight="22dp" android:gravity="center" />
                    </LinearLayout>
                </LinearLayout>
            </FrameLayout>
            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:baselineAligned="false" android:layout_marginTop="20dp" android:gravity="center_vertical">
                <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_classes" style="@style/StudyFlow.Home.Text" android:layout_width="0dp" android:layout_height="wrap_content" android:text="@string/home_classes" android:textSize="17sp" android:fontFamily="@font/inter_bold" android:textColor="@color/studyflow_ink" android:layout_weight="1" />
                <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_class_count" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="match_parent" android:text="@string/home_class_count" android:textSize="12sp" android:fontFamily="@font/inter_semibold" android:textColor="@color/studyflow_primary" android:clickable="true" android:focusable="true" android:background="?attr/selectableItemBackground" android:gravity="center_vertical" />
            </LinearLayout>
            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:baselineAligned="false" android:id="@+id/home_class_card" android:minHeight="66dp" android:gravity="center_vertical" android:paddingStart="14dp" android:paddingEnd="14dp" android:paddingTop="14dp" android:paddingBottom="14dp" android:layout_marginTop="12dp" android:background="@drawable/bg_home_class">
                <LinearLayout android:layout_width="62dp" android:layout_height="wrap_content" android:orientation="vertical">
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_start" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_start" android:textSize="13sp" android:fontFamily="@font/inter_bold" android:textColor="@color/studyflow_primary" />
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_end" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_end" android:textSize="10sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_muted" android:layout_marginTop="7dp" />
                </LinearLayout>
                <View android:layout_width="3dp" android:layout_height="38dp" android:layout_marginEnd="12dp" android:background="@drawable/bg_home_divider" android:importantForAccessibility="no" />
                <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:layout_weight="1" android:layout_marginEnd="8dp">
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_calculus" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_calculus" android:textSize="13sp" android:fontFamily="@font/inter_semibold" android:textColor="@color/studyflow_ink" />
                    <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_room" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_room" android:textSize="11sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_muted" android:layout_marginTop="7dp" />
                </LinearLayout>
                <androidx.appcompat.widget.AppCompatImageView android:layout_width="19dp" android:layout_height="19dp" android:src="@drawable/ic_home_broadcast" android:importantForAccessibility="no" />
            </LinearLayout>
            <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_up_next" style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/home_up_next" android:textSize="11sp" android:fontFamily="@font/inter_regular" android:textColor="@color/studyflow_muted" android:layout_marginTop="14dp" />
        </LinearLayout>
    </androidx.core.widget.NestedScrollView>
    <FrameLayout android:id="@+id/home_add_container" android:layout_width="54dp" android:layout_height="54dp" android:clipChildren="false" android:clipToPadding="false" android:layout_marginEnd="24dp" android:layout_marginBottom="24dp" app:layout_constraintBottom_toTopOf="@id/home_navigation" app:layout_constraintEnd_toEndOf="parent">
        <ImageView android:layout_width="94dp" android:layout_height="94dp" android:layout_gravity="center" android:translationY="8dp" android:src="@drawable/home_plus_shadow" android:importantForAccessibility="no" />
        <androidx.appcompat.widget.AppCompatImageButton android:id="@+id/home_add" android:layout_width="54dp" android:layout_height="54dp" android:src="@drawable/ic_home_plus" android:padding="16dp" android:background="@drawable/bg_home_plus" android:contentDescription="@string/home_add" />
    </FrameLayout>
    <FrameLayout android:id="@+id/home_navigation" android:layout_width="0dp" android:layout_height="wrap_content" android:background="@color/studyflow_white" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintEnd_toEndOf="parent">
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:baselineAligned="false" android:paddingStart="10dp" android:paddingEnd="10dp">
            <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:id="@+id/home_tab_home" android:layout_weight="1" android:minHeight="54dp" android:paddingTop="8dp" android:paddingBottom="2dp" android:gravity="center_horizontal" android:contentDescription="@string/home_nav_home" android:importantForAccessibility="yes" android:clickable="true" android:focusable="true" android:background="?attr/selectableItemBackground">
                <FrameLayout android:layout_width="48dp" android:layout_height="28dp" android:layout_gravity="center_horizontal" android:background="@drawable/bg_home_selected">
                    <androidx.appcompat.widget.AppCompatImageView android:layout_width="21dp" android:layout_height="21dp" android:src="@drawable/ic_home_home" android:importantForAccessibility="no" android:layout_gravity="center" />
                </FrameLayout>
                <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_nav_home" style="@style/StudyFlow.Home.Text" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/home_nav_home" android:textSize="10sp" android:fontFamily="@font/inter_bold" android:textColor="@color/studyflow_primary" android:layout_marginTop="4dp" android:gravity="center" />
            </LinearLayout>
            <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:id="@+id/home_tab_schedule" android:layout_weight="1" android:minHeight="54dp" android:paddingTop="8dp" android:paddingBottom="2dp" android:gravity="center_horizontal" android:contentDescription="@string/home_nav_schedule" android:importantForAccessibility="yes" android:clickable="true" android:focusable="true" android:background="?attr/selectableItemBackground">
                <FrameLayout android:layout_width="48dp" android:layout_height="28dp" android:layout_gravity="center_horizontal">
                    <androidx.appcompat.widget.AppCompatImageView android:layout_width="21dp" android:layout_height="21dp" android:src="@drawable/ic_home_schedule" android:importantForAccessibility="no" android:layout_gravity="center" />
                </FrameLayout>
                <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_nav_schedule" style="@style/StudyFlow.Home.Text" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/home_nav_schedule" android:textSize="10sp" android:fontFamily="@font/inter_medium" android:textColor="@color/studyflow_muted" android:layout_marginTop="4dp" android:gravity="center" />
            </LinearLayout>
            <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:id="@+id/home_tab_tasks" android:layout_weight="1" android:minHeight="54dp" android:paddingTop="8dp" android:paddingBottom="2dp" android:gravity="center_horizontal" android:contentDescription="@string/home_nav_tasks" android:importantForAccessibility="yes" android:clickable="true" android:focusable="true" android:background="?attr/selectableItemBackground">
                <FrameLayout android:layout_width="48dp" android:layout_height="28dp" android:layout_gravity="center_horizontal">
                    <androidx.appcompat.widget.AppCompatImageView android:layout_width="21dp" android:layout_height="21dp" android:src="@drawable/ic_home_tasks" android:importantForAccessibility="no" android:layout_gravity="center" />
                </FrameLayout>
                <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_nav_tasks" style="@style/StudyFlow.Home.Text" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/home_nav_tasks" android:textSize="10sp" android:fontFamily="@font/inter_medium" android:textColor="@color/studyflow_muted" android:layout_marginTop="4dp" android:gravity="center" />
            </LinearLayout>
            <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:id="@+id/home_tab_notes" android:layout_weight="1" android:minHeight="54dp" android:paddingTop="8dp" android:paddingBottom="2dp" android:gravity="center_horizontal" android:contentDescription="@string/home_nav_notes" android:importantForAccessibility="yes" android:clickable="true" android:focusable="true" android:background="?attr/selectableItemBackground">
                <FrameLayout android:layout_width="48dp" android:layout_height="28dp" android:layout_gravity="center_horizontal">
                    <androidx.appcompat.widget.AppCompatImageView android:layout_width="21dp" android:layout_height="21dp" android:src="@drawable/ic_home_notes" android:importantForAccessibility="no" android:layout_gravity="center" />
                </FrameLayout>
                <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_nav_notes" style="@style/StudyFlow.Home.Text" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/home_nav_notes" android:textSize="10sp" android:fontFamily="@font/inter_medium" android:textColor="@color/studyflow_muted" android:layout_marginTop="4dp" android:gravity="center" />
            </LinearLayout>
            <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:orientation="vertical" android:id="@+id/home_tab_profile" android:layout_weight="1" android:minHeight="54dp" android:paddingTop="8dp" android:paddingBottom="2dp" android:gravity="center_horizontal" android:contentDescription="@string/home_nav_profile" android:importantForAccessibility="yes" android:clickable="true" android:focusable="true" android:background="?attr/selectableItemBackground">
                <FrameLayout android:layout_width="48dp" android:layout_height="28dp" android:layout_gravity="center_horizontal">
                    <androidx.appcompat.widget.AppCompatImageView android:layout_width="21dp" android:layout_height="21dp" android:src="@drawable/ic_home_profile" android:importantForAccessibility="no" android:layout_gravity="center" />
                </FrameLayout>
                <androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_nav_profile" style="@style/StudyFlow.Home.Text" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/home_nav_profile" android:textSize="10sp" android:fontFamily="@font/inter_medium" android:textColor="@color/studyflow_muted" android:layout_marginTop="4dp" android:gravity="center" />
            </LinearLayout>
        </LinearLayout>
        <View android:layout_width="match_parent" android:layout_height="1dp" android:background="@color/studyflow_outline" android:importantForAccessibility="no" />
    </FrameLayout>
</androidx.constraintlayout.widget.ConstraintLayout>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\home_strings.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="home_date">MONDAY, OCTOBER 5</string>
    <string name="home_greeting">Hi, Aruzhan ✦</string>
    <string name="home_subtitle">Let’s make today a little lighter.</string>
    <string name="home_week">YOUR LAST 7 DAYS</string>
    <string name="home_momentum">Great momentum.</string>
    <string name="home_hours">9 of 12 focused hours</string>
    <string name="home_percent">75%</string>
    <string name="home_done">6 / 10 tasks done</string>
    <string name="home_streak">✦ 5-day streak</string>
    <string name="home_next_deadline">NEXT DEADLINE</string>
    <string name="home_problem">Problem set 04</string>
    <string name="home_due">Calculus II · Tue, 18:00</string>
    <string name="home_countdown">1d 7h</string>
    <string name="home_remaining">36m remaining</string>
    <string name="home_priorities">Your priorities</string>
    <string name="home_see_all">See all</string>
    <string name="home_problem_detail">Calculus II · 1d 7h left</string>
    <string name="home_high">High</string>
    <string name="home_diagram">ER diagram project</string>
    <string name="home_diagram_detail">Database Systems · 2d 13h left</string>
    <string name="home_medium">Medium</string>
    <string name="home_classes">Today’s classes</string>
    <string name="home_class_count">4 classes</string>
    <string name="home_start">10:00</string>
    <string name="home_end">11:20</string>
    <string name="home_calculus">Calculus II</string>
    <string name="home_room">B-204 · In class now</string>
    <string name="home_up_next">Up next · 13:00 Physics II · Lab C-112</string>
    <string name="home_nav_home">Home</string>
    <string name="home_nav_schedule">Schedule</string>
    <string name="home_nav_tasks">Tasks</string>
    <string name="home_nav_notes">Notes</string>
    <string name="home_nav_profile">Profile</string>
    <string name="home_notifications">Notifications</string>
    <string name="home_add">Add</string>
    <string name="home_check_problem">Mark Problem set 04 as completed</string>
    <string name="home_check_diagram">Mark ER diagram project as completed</string>
    <string name="home_progress_description">Weekly focus progress: 75 percent, 9 of 12 hours</string>
</resources>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\home_styles.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.StudyFlowApp.Home" parent="Theme.StudyFlowApp.Onboarding">
        <item name="android:windowBackground">@color/studyflow_register_background</item>
    </style>
    <style name="StudyFlow.Home.Text" parent="StudyFlow.Onboarding.Text">
    </style>
</resources>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values-v28\home_styles.xml`

Действие: создать файл по указанному пути.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="StudyFlow.Home.Text" parent="StudyFlow.Onboarding.Text">
        <item name="android:fallbackLineSpacing">false</item>
    </style>
</resources>
```

## 5. Проверка

Сборка assembleDebug и lintDebug завершились без ошибок. В эмуляторе проверены переходы из обеих форм, блокировка Log In при коротком пароле, блокировка регистрации без согласия, переключение галочки задачи, прокрутка и закреплённая навигация на небольшом экране. Настройки размера экрана и шрифта после проверки восстановлены.

Для сравнения с Figma сохранён Home-390x1008.png. Дополнительно сохранены Home-small-top-font130.png и Home-small-bottom-font130.png для экрана 360 × 640 dp со шрифтом 130%. Lint оставляет рекомендации о небольших размерах текста из макета и сложности иерархии; ошибок компиляции и Lint нет.

При запуске ты должна увидеть свой splash и onboarding, а после заполнения Login или Register — Home с синим градиентом, кольцом 75%, двумя задачами и нижним меню. Если внешний вид на твоём телефоне отличается, пришли скриншот для сравнения.
