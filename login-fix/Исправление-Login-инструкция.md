# Исправление полей Login

Изменения уже установлены в проект StudyFlowApp; вручную вставлять код не нужно.

## Что исправлено

Удалены hint-подсказки email и пароля: при новом открытии оба поля пусты. Названия Email address и Password над полями сохранены.

В Gboard на эмуляторе был выключен показ экранной клавиатуры при подключённой физической клавиатуре. Вместо букв появлялась боковая панель. В настройках Gboard → Physical keyboard включён Show on-screen keyboard. Также включён системный показ клавиатуры при подключённой физической клавиатуре. Это настройка эмулятора; она не переносится вместе с APK на другое устройство. В коде формы нажатие на любое поле явно запрашивает экранную клавиатуру. Временные изменения для проверки гипотезы о рукописном вводе убраны.

## Как проверить

1. В Android Studio открой проект `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`.
2. Выбери `app` и эмулятор, нажми зелёную кнопку **Run ▶**.
3. После splash нажми **Log In** на onboarding. Оба поля должны быть пустыми.
4. Нажми внутри поля **Email address** — снизу должна появиться обычная клавиатура. Введи тестовый адрес.
5. Закрой клавиатуру системной кнопкой «Назад» и снова нажми поле email: клавиатура должна открыться повторно.
6. Нажми поле Password и введи тестовый пароль. Значок глаза по-прежнему показывает/скрывает введённый текст.

Если на другом эмуляторе появится такая же боковая панель: нажми её меню → Settings → Physical keyboard → включи Show on-screen keyboard. Из главного экрана настроек Gboard путь такой же: Physical keyboard → Show on-screen keyboard.

Дополнительное исправление после повторного появления панели: Gboard → Write in text fields → Use stylus to write in text fields → выключено. Этот режим был включён независимо от настройки физической клавиатуры. После его отключения проверены события mouse, stylus и touchscreen; на скриншотах отображается обычная клавиатура. Параметр Show toolbar в разделе Physical keyboard недоступен при включённом Show on-screen keyboard, поэтому отдельно он не менялся. Настройки касаются только этого эмулятора; код приложения на этом этапе не изменялся.

Сборка assembleDebug и lintDebug успешны. В эмуляторе проверены пустые поля, открытие и повторное открытие клавиатуры email, клавиатура пароля, переключатель видимости и повторный вход на экран. Обычная клавиатура дополнительно проверена по скриншотам. Тестовые значения затем убраны повторным открытием экрана. Остальные исходные файлы сохранены.

## Файлы и полный код

Изменены только следующие три файла. Резервные копии лежат в папке `backup` рядом с этой инструкцией. Для ручного восстановления открой указанный файл, удали его содержимое и вставь соответствующий полный код. Новые файлы создавать не требуется.


### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\LoginActivity.kt`

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

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_login.xml`

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
                        android:layout_width="match_parent" android:layout_height="match_parent"
                        android:inputType="textEmailAddress" android:imeOptions="actionNext" android:autofillHints="emailAddress" android:nextFocusForward="@id/login_password" />
                    <ImageView android:layout_width="19dp" android:layout_height="19dp" android:layout_gravity="end|center_vertical" android:layout_marginEnd="14dp" android:src="@drawable/ic_login_email" android:contentDescription="@null" android:importantForAccessibility="no" />
                </FrameLayout>
                <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="20dp" android:text="@string/login_password_label" android:labelFor="@id/login_password" />
                <FrameLayout android:layout_width="match_parent" android:layout_height="52dp" android:layout_marginTop="8dp" android:background="@drawable/bg_login_field" android:addStatesFromChildren="true">
                    <androidx.appcompat.widget.AppCompatEditText android:id="@+id/login_password" style="@style/StudyFlow.Login.Input"
                        android:layout_width="match_parent" android:layout_height="match_parent"
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

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\login_strings.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="login_brand">STUDYFLOW</string>
    <string name="login_title">Welcome back.\nFind your flow.</string>
    <string name="login_description">Your classes, goals and ideas.\nAll right where you left them.</string>
    <string name="login_email_label">Email address</string>
    <string name="login_password_label">Password</string>
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