# StudyFlow — третий экран «Never Miss a Class»

## 1. Анализ дизайна

Это второй шаг onboarding и третий экран приложения после Splash и
«Track Every Deadline». Основа — ваш SVG 390 × 844 и PNG 1026 × 840.
Иллюстрация скопирована без изменений. Тексты, карточки и кнопки остаются
отдельными Android Views в XML.

Сохраняются боковые поля 24dp, карточка 342 × 332 с радиусом 30dp,
полупрозрачная подпись, заголовок Inter Bold 32sp, описание Inter 14sp,
кнопка высотой 52dp с радиусом 14dp и цветом #4564ED. Все общие фоны,
шрифты, цвета, иконка стрелки и тень кнопки используются из предыдущего этапа.

Отличия нового экрана:

- Иллюстрация расписания с меткой места.
- Подписи «Right class. Right place.» и «Calculus II · Room B-204».
- Плашка шага 02 шириной 208dp.
- Заголовок «Never Miss a Class» и новые две строки описания.
- Средний индикатор активен: ширина 26dp; крайние — по 7dp.

## 2. Какие файлы нужны

Папка проекта: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`.
Изменён только существующий `OnboardingActivity.kt`. Добавлены три файла:
разметка, строки и иллюстрация. Манифест, MainActivity, исправление Splash,
Gradle и ресурсы первого onboarding не менялись.

- [app/src/main/java/com/example/studyflowapp/OnboardingActivity.kt](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/java/com/example/studyflowapp/OnboardingActivity.kt>)
- [app/src/main/res/drawable-xxhdpi/onboarding_classes_illustration.png](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/drawable-xxhdpi/onboarding_classes_illustration.png>)
- [app/src/main/res/layout/activity_onboarding_classes.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/layout/activity_onboarding_classes.xml>)
- [app/src/main/res/values/onboarding_classes_strings.xml](<C:/Users/admin/AndroidStudioProjects/StudyFlowApp/app/src/main/res/values/onboarding_classes_strings.xml>)

Одна OnboardingActivity показывает соответствующий XML по номеру страницы,
переданному через Intent. Этот номер сохраняется при пересоздании Activity.
При переходе предыдущий экран остаётся в стандартном стеке Android, поэтому
системная кнопка «Назад» возвращает на первый onboarding. Повторное быстрое
нажатие Get Started не должно создавать несколько копий следующего экрана.

## 3. Пошаговая инструкция

Файлы уже установлены в проект. Копировать код повторно не нужно.

1. Откройте **StudyFlowApp** в Android Studio.
2. Вверху выберите **app** и **Medium Phone API 37.0**.
3. Нажмите **Run ▶**.
4. После Splash появится «Track Every Deadline».
5. Нажмите **Get Started** — откроется «Never Miss a Class».
6. Нажмите системную кнопку или выполните жест **Назад** для возврата на первый экран.

Для просмотра XML откройте **app → res → layout → activity_onboarding_classes.xml**
и выберите **Split**. Kotlin-код находится в **app → kotlin+java →
com.example.studyflowapp → OnboardingActivity**.

Переход по Get Started на первом экране временно используется для просмотра
готовых макетов. На втором onboarding кнопки Get Started, Skip и Log In пока
дают только визуальную реакцию. Следующие переходы подключим после получения
соответствующих макетов. Свайпы между страницами пока не добавлены.

Если потребуется ручное восстановление, архив `StudyFlowApp-classes.zip`
содержит только изменения этого этапа и применяется поверх готового проекта
с предыдущими экранами. Папка `app` в архиве соответствует папке `app` проекта.

## 4. Готовый код

### OnboardingActivity.kt

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\OnboardingActivity.kt`

**Действие:** Открыть существующий файл, удалить старое содержимое и вставить полный код ниже.

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
        val pageIndex = intent.getIntExtra(EXTRA_PAGE_INDEX, 0).coerceIn(0, 1)
        setContentView(
            if (pageIndex == 1) R.layout.activity_onboarding_classes
            else R.layout.activity_onboarding
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
        // Temporary navigation between the two completed onboarding layouts.
        if (pageIndex == 0) {
            findViewById<View>(R.id.onboarding_get_started).setOnClickListener {
                if (!openingNextPage) {
                    openingNextPage = true
                    startActivity(
                        Intent(this, OnboardingActivity::class.java)
                            .putExtra(EXTRA_PAGE_INDEX, 1)
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

### onboarding_classes_illustration.png

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable-xxhdpi\onboarding_classes_illustration.png`

**Действие:** скопировать PNG из архива в папку `res/drawable-xxhdpi`. Если папки нет, создать её. Имя файла должно быть `onboarding_classes_illustration.png`. Вручную вводить код изображения не нужно.

### activity_onboarding_classes.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\layout\activity_onboarding_classes.xml`

**Действие:** В папке res/layout создать Layout Resource File с именем activity_onboarding_classes.xml и вставить полный код ниже.

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
                android:src="@drawable/onboarding_classes_illustration"
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
                    android:text="@string/onboarding_classes_card_title"
                    android:textSize="12sp" />

                <androidx.appcompat.widget.AppCompatTextView
                    style="@style/StudyFlow.Onboarding.Text"
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:layout_marginTop="4dp"
                    android:text="@string/onboarding_classes_card_detail"
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
            android:text="@string/onboarding_classes_badge"
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
            android:text="@string/onboarding_classes_title"
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
            android:text="@string/onboarding_classes_description"
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
                android:layout_width="26dp"
                android:layout_height="7dp"
                android:layout_marginStart="6dp"
                android:background="@drawable/bg_onboarding_page_active" />
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

### onboarding_classes_strings.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\onboarding_classes_strings.xml`

**Действие:** В папке res/values создать Values Resource File с именем onboarding_classes_strings.xml и вставить полный код ниже.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="onboarding_classes_card_title">Right class. Right place.</string>
    <string name="onboarding_classes_card_detail">Calculus II · Room B-204</string>
    <string name="onboarding_classes_badge">02 / YOUR ACADEMIC LIFE, SIMPLIFIED</string>
    <string name="onboarding_classes_title">Never Miss a Class</string>
    <string name="onboarding_classes_description">See your classes, rooms and lecturers at a glance.\nArrive ready, with your day already mapped out.</string>
</resources>

```

## 5. Проверка

- `assembleDebug` и `lintDebug` выполнены успешно: ошибок 0, предупреждений 12.
- Запуск приложения и переход с первого onboarding на второй проверены на API 37.
- Проверены возврат назад и повторный переход вперёд.
- При смене размера эмулятора второй экран сохраняется.
- При 390 × 844dp карточка занимает x=24, y=116, ширину 342, высоту 332;
  плашка занимает x=24, y=474, ширину 208, высоту 22.
- При 360 × 640dp и шрифте 130% Get Started и Log In доступны после прокрутки.
- Размер, плотность и масштаб текста эмулятора после проверки восстановлены.
- Контрольные суммы 52 других файлов исходников совпали с состоянием
  до этого этапа. Это включает исправленный MainActivity и тему запуска Splash.

Отдельного запуска на API 24 не было: совместимость с минимальной версией
проверена сборкой и Lint. Системные часы, значки и жестовая полоска принадлежат
Android и могут отличаться от нарисованных в Figma.

Предупреждения Lint:

- `VectorRaster`: Limit vector icons sizes to 200×200 to keep icon drawing fast; see https://developer.android.com/studio/write/vector-asset-studio#when for more
- `VectorRaster`: Limit vector icons sizes to 200×200 to keep icon drawing fast; see https://developer.android.com/studio/write/vector-asset-studio#when for more
- `VectorRaster`: Limit vector icons sizes to 200×200 to keep icon drawing fast; see https://developer.android.com/studio/write/vector-asset-studio#when for more
- `AndroidGradlePluginVersion`: A newer version of com.android.application than 9.4.1 is available: 9.5.0
- `UnusedResources`: The resource `R.color.black` appears to be unused
- `UnusedResources`: The resource `R.color.white` appears to be unused
- `UnusedResources`: The resource `R.drawable.ic_studyflow_launch` appears to be unused
- `IconMissingDensityFolder`: Missing density variation folders in `src\main\res`: drawable-hdpi, drawable-mdpi, drawable-xhdpi
- `SmallSp`: Avoid using sizes smaller than `11sp`: `10sp`
- `SmallSp`: Avoid using sizes smaller than `11sp`: `10sp`
- `SmallSp`: Avoid using sizes smaller than `11sp`: `10sp`
- `SmallSp`: Avoid using sizes smaller than `11sp`: `10sp`

Предупреждения SmallSp относятся к размерам 10sp, заданным в ваших макетах.
Эти размеры сохранены. Новые зависимости и обновления инструментов не добавлялись.

Снимки результата находятся рядом с инструкцией:

- `Never-Miss-a-Class-390x844.png` — размер макета, снимок в масштабе 3×.
- `Never-Miss-a-Class-emulator.png` — обычные настройки вашего эмулятора.
- `Never-Miss-a-Class-small-font130.png` — небольшой экран с увеличенным текстом.
