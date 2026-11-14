# StudyFlow — четвёртый экран «Make Time Work for You»

## 1. Анализ дизайна

Это третий шаг onboarding и четвёртый экран приложения с учётом Splash.
Ваш SVG имеет размер **390 × 859**, тогда как предыдущие onboarding-макеты —
390 × 844. Увеличенную высоту и переносы текста учли при вёрстке.

Использована ваша иллюстрация часов с книгами, PNG 1026 × 840 без изменений.
Тексты, карточка-пример, индикаторы и кнопки созданы отдельными Android Views.
Повторно используются Inter, цвета, фоны, стрелка и тень кнопки из предыдущих экранов.

| Элемент | Параметры |
|---|---|
| Боковые поля | 24dp |
| Карточка иллюстрации | 342 × 332, радиус 30dp |
| Плашка шага | 03; 208 × 22 |
| Заголовок | Inter Bold 32sp; две строки; шаг строк 36sp |
| Описание | Inter Regular 14sp; три строки; шаг строк около 21sp |
| Индикаторы | 7, 7 и 26dp; активен третий |
| Get Started | 342 × 52 при ширине экрана 390dp; радиус 14dp |

Заголовок переносится после «for». В описании первая строка заканчивается
«Turn», вторая — «actually», третья содержит «reach.». На более узких экранах
или с увеличенным шрифтом разрешены дополнительные переносы и прокрутка.

## 2. Какие файлы нужны

Папка проекта: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`.
Изменён только `OnboardingActivity.kt`; добавлены разметка, строки и PNG.
Манифест, Gradle, предыдущие XML-экраны и исправленный Splash не менялись.

- [app/src/main/java/com/example/studyflowapp/OnboardingActivity.kt](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/java/com/example/studyflowapp/OnboardingActivity.kt>)
- [app/src/main/res/drawable-xxhdpi/onboarding_focus_illustration.png](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable-xxhdpi/onboarding_focus_illustration.png>)
- [app/src/main/res/layout/activity_onboarding_focus.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/layout/activity_onboarding_focus.xml>)
- [app/src/main/res/values/onboarding_focus_strings.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/values/onboarding_focus_strings.xml>)

OnboardingActivity выбирает одну из трёх XML-разметок по номеру шага в Intent.
Get Started на первых двух шагах открывает следующий. На последнем шаге эта
кнопка пока даёт только реакцию на нажатие. Системная кнопка «Назад» возвращает
к предыдущему шагу. Номер текущей страницы сохраняется при пересоздании Activity.

## 3. Пошаговая инструкция

Изменения уже установлены. Вставлять код повторно не нужно.

1. В Android Studio откройте **StudyFlowApp**.
2. Выберите конфигурацию **app** и **Medium Phone API 37.0**.
3. Нажмите **Run ▶**.
4. После Splash появится «Track Every Deadline».
5. Нажмите **Get Started** — откроется «Never Miss a Class».
6. Нажмите **Get Started** ещё раз — откроется «Make Time Work for You».
7. Системной кнопкой или жестом **Назад** можно вернуться к предыдущим шагам.

Разметка находится в **app → res → layout → activity_onboarding_focus.xml**.
Для просмотра вместе с кодом выберите **Split**.
Kotlin-файл находится в **app → kotlin+java → com.example.studyflowapp → OnboardingActivity**.

Skip и Log In пока имеют только визуальную реакцию. Регистрация, авторизация,
сохранение данных и загрузка с сервера не добавлены. Свайпы между страницами
пока не подключены. Строка «9 of 12 hours» — демонстрационный текст из макета.

Архив `StudyFlowApp-focus.zip` содержит только четыре файла нового этапа:
он применяется поверх уже готового проекта с предыдущими экранами.

## 4. Готовый код

### OnboardingActivity.kt

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\OnboardingActivity.kt`

**Действие:** Открыть существующий файл, удалить старое содержимое и вставить весь код ниже.

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
        // Skip, Log In and the final page CTA use ripple feedback only.
    }

    override fun onResume() {
        super.onResume()
        openingNextPage = false
    }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density + 0.5f).toInt()
}

```

### onboarding_focus_illustration.png

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\onboarding_focus_illustration.png`

**Действие:** скопировать PNG из архива в `res/drawable-xxhdpi` с именем `onboarding_focus_illustration.png`. Вручную вводить код изображения не нужно.

### activity_onboarding_focus.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_onboarding_focus.xml`

**Действие:** В res/layout создать Layout Resource File с именем activity_onboarding_focus.xml и вставить весь код ниже.

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
                android:src="@drawable/onboarding_focus_illustration"
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
                    android:text="@string/onboarding_focus_card_title"
                    android:textSize="12sp" />

                <androidx.appcompat.widget.AppCompatTextView
                    style="@style/StudyFlow.Onboarding.Text"
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:layout_marginTop="4dp"
                    android:text="@string/onboarding_focus_card_detail"
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
            android:minWidth="208dp"
            android:paddingStart="9dp"
            android:paddingEnd="9dp"
            android:text="@string/onboarding_focus_badge"
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
            android:text="@string/onboarding_focus_title"
            android:textSize="32sp"
            app:lineHeight="36sp"
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
            android:text="@string/onboarding_focus_description"
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
                android:layout_width="7dp"
                android:layout_height="7dp"
                android:background="@drawable/bg_onboarding_page_inactive" />
            <View
                android:layout_width="7dp"
                android:layout_height="7dp"
                android:layout_marginStart="6dp"
                android:background="@drawable/bg_onboarding_page_inactive" />
            <View
                android:layout_width="26dp"
                android:layout_height="7dp"
                android:layout_marginStart="6dp"
                android:background="@drawable/bg_onboarding_page_active" />
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

### onboarding_focus_strings.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\onboarding_focus_strings.xml`

**Действие:** В res/values создать Values Resource File с именем onboarding_focus_strings.xml и вставить весь код ниже.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="onboarding_focus_card_title">A little focus goes a long way</string>
    <string name="onboarding_focus_card_detail">Weekly focus goal · 9 of 12 hours</string>
    <string name="onboarding_focus_badge">03 / YOUR ACADEMIC LIFE, SIMPLIFIED</string>
    <string name="onboarding_focus_title">Make Time Work for\nYou</string>
    <string name="onboarding_focus_description">Build a study rhythm that fits your life. Turn\nfocused moments into goals you can actually\nreach.</string>
</resources>

```

## 5. Проверка

- `assembleDebug` и `lintDebug` завершились успешно: ошибок 0, предупреждений 14.
- Приложение проверено в эмуляторе API 37.
- Проверены переходы через все три страницы onboarding, два возврата назад
  и повторные переходы вперёд.
- На размере 390 × 859dp проверены переносы текста и координаты:
  карточка — x=24, y=116, ширина 342, высота 332;
  плашка — x=24, y=474, ширина 208, высота 22;
  кнопка — x=24, y≈718, ширина 342, высота 52.
- На экране 360 × 640dp с текстом 130% Get Started и Log In доступны после прокрутки.
- После изменения размеров эмулятора сохраняется третий шаг onboarding.
- Исходные размер, плотность и масштаб текста эмулятора восстановлены.
- Контрольные суммы 55 остальных исходных файлов не изменились,
  включая MainActivity и тему исправленного Splash.

Отдельного запуска на API 24 не было; совместимость с minSdk 24 проверена
сборкой и Lint. Для межстрочного интервала применён совместимый атрибут
`app:lineHeight` существующего AppCompatTextView.

Предупреждения Lint:

- `VectorRaster` — 3: Limit vector icons sizes to 200×200 to keep icon drawing fast; see https://developer.android.com/studio/write/vector-asset-studio#when for more
- `AndroidGradlePluginVersion` — 1: A newer version of com.android.application than 9.4.1 is available: 9.5.0
- `UnusedResources` — 3: The resource `R.color.black` appears to be unused
- `IconMissingDensityFolder` — 1: Missing density variation folders in `src\main\res`: drawable-hdpi, drawable-mdpi, drawable-xhdpi
- `SmallSp` — 6: Avoid using sizes smaller than `11sp`: `10sp`

SmallSp относится к размерам 10sp из ваших макетов. Эти размеры сохранены,
как и версии зависимостей проекта. Предупреждения не препятствуют сборке.

Снимки рядом с инструкцией:

- `Make-Time-Work-for-You-390x859.png` — размер макета, снимок в масштабе 3×.
- `Make-Time-Work-for-You-emulator.png` — обычный размер вашего эмулятора.
- `Make-Time-Work-for-You-small-font130.png` — небольшой экран с увеличенным текстом.

Системные часы, значки и нижняя жестовая полоска отображаются Android и могут
отличаться от панелей iPhone, нарисованных в макете.
