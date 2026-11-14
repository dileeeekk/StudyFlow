# Register — только University

Изменения уже установлены в проект StudyFlowApp.

## Что изменилось

Удалены Year и Group. University теперь обычное пустое поле для ввода названия университета без стрелки и без текста-подсказки. Карточка стала короче на 91 dp; чекбокс, кнопка и ссылка ниже поднялись вместе с ней. Тень пересоздана под новую высоту карточки, чтобы сохранить её скругления и размытие.

На клавиатуре поле пароля теперь предлагает «Далее» к University, а University — «Готово» для закрытия клавиатуры. Новое поле участвует в существующей прокрутке формы при появлении клавиатуры. Сохранение профиля и регистрация не добавлены.

## Как проверить

1. В Android Studio открой StudyFlowApp и нажми Run ▶.
2. Открой Login → Create an account.
3. Под паролем должно остаться только пустое поле University; Year и Group отсутствуют.
4. Нажми University и введи название. Клавиатура должна открыться, введённые буквы — появиться в поле.

Сборка assembleDebug и lintDebug прошла без ошибок. В эмуляторе проверены отсутствие Year/Group, пустое начальное значение, ввод текста в University, клавиатура и возврат на Login. Все остальные исходные файлы сохранены.

## Файлы и полный код

Ниже актуальный полный код. Вручную копировать его сейчас не требуется. Для восстановления открой указанный файл, выдели старое содержимое целиком и замени кодом ниже. Новые файлы создавать не нужно. Предыдущие версии сохранены в папке backup рядом с этой инструкцией.


### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\RegisterActivity.kt`


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
        val university = findViewById<EditText>(R.id.register_university)
        for (field in listOf(findViewById<EditText>(R.id.register_name), email, password, university)) {
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
        university.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) { closeKeyboard(); true } else false
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```


### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\register_card_shadow.png`


Заменить PNG готовым файлом из архива по этому же относительному пути.


### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_register.xml`


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
            android:imeOptions="actionNext" android:nextFocusForward="@id/register_university" android:autofillHints="newPassword" android:saveEnabled="false" />
        <androidx.appcompat.widget.AppCompatImageButton android:id="@+id/register_password_toggle" android:layout_width="48dp" android:layout_height="match_parent" android:layout_gravity="end"
        android:background="?attr/selectableItemBackgroundBorderless" android:padding="0dp" android:scaleType="center" android:src="@drawable/ic_login_eye_off" android:contentDescription="@string/login_show_password" />
    </FrameLayout>
                <androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Text" android:layout_width="match_parent" android:layout_height="wrap_content"
                    android:layout_marginTop="7dp" android:text="@string/register_password_helper" android:textSize="10sp" android:textColor="@color/studyflow_register_helper" />
<androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Login.Label"
        android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="16dp"
        android:text="@string/register_university_label" android:labelFor="@id/register_university" /><androidx.appcompat.widget.AppCompatEditText
                    android:id="@+id/register_university"
                    style="@style/StudyFlow.Login.Input"
                    android:layout_width="match_parent"
                    android:layout_height="52dp"
                    android:layout_marginTop="8dp"
                    android:background="@drawable/bg_login_field"
                    android:backgroundTint="@null"
                    android:paddingEnd="14dp"
                    android:inputType="textCapWords"
                    android:imeOptions="actionDone" />
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


### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\register_strings.xml`


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
    <string name="register_agreement">I agree to the <font color="#4564ED">Terms of Service</font> and <font color="#4564ED">Privacy Policy</font>.</string>
    <string name="register_submit">Create Account</string>
    <string name="register_member">"Already a member? "</string>
</resources>
```
