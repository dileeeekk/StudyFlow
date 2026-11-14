# Исправление показа Splash

## Причина

Android 12 и новее сначала показывал свою системную заставку с центральным логотипом.
Таймер перехода в MainActivity запускался в onStart ещё до её исчезновения.
В последних запусках после появления макета оставалось около 0,8 секунды до перехода.

## Что исправлено

Системная центральная иконка заменена прозрачным drawable. После подготовки окна
системная заставка снимается без дополнительной анимации. Отсчёт 1,5 секунды
начинается после появления разметки и снятия системной заставки. Уход приложения
в фон отменяет ожидающий переход. Макеты Splash и onboarding не менялись.

Показ длительностью 1,5 секунды — временное поведение этапа вёрстки, не настоящая
загрузка данных. Когда появится загрузка, переход будет зависеть от её завершения.

До готовности окна Android всё равно может кратко показывать однотонный синий фон.
Системная заставка не поддерживает полный произвольный XML-макет с градиентом:
[документация Android](https://developer.android.com/develop/ui/views/launch/splash-screen).

## Запуск и проверка

Исправление уже установлено; вставлять код повторно не нужно.

1. В Android Studio нажмите **Stop ■**, если приложение запущено.
2. Выберите конфигурацию **app** и эмулятор **Medium Phone API 37.0**.
3. Нажмите **Run ▶**.
4. Вы должны увидеть полный градиентный Splash с надписью StudyFlow,
   а после его показа — onboarding с календарём.

`assembleDebug` и `lintDebug` завершились без ошибок. На эмуляторе API 37
сохранены два последовательных кадра полного Splash, затем подтверждено
открытие OnboardingActivity. Проверка на отдельном Android 7 устройстве не выполнялась.

Это исправление новее кода MainActivity из ранее выданного архива onboarding.
При ручном восстановлении используйте версии ниже поверх готового проекта.

## Файлы и полный код

### MainActivity.kt

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\MainActivity.kt`

**Действие:** Открыть существующий файл и полностью заменить содержимое.

```kotlin
package com.example.studyflowapp

import android.content.Intent
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.doOnPreDraw

class MainActivity : AppCompatActivity() {
    private val handler = Handler(Looper.getMainLooper())
    private var activityStarted = false
    private var contentDrawn = false
    private var systemSplashDismissed = Build.VERSION.SDK_INT < Build.VERSION_CODES.S

    private val openOnboarding = Runnable {
        if (activityStarted && contentDrawn && systemSplashDismissed) {
            startActivity(Intent(this, OnboardingActivity::class.java))
            finish()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.dark(Color.TRANSPARENT)
        )
        setContentView(R.layout.activity_main)
        val content = findViewById<View>(R.id.main)

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            splashScreen.setOnExitAnimationListener { systemSplash ->
                systemSplash.remove()
                content.postOnAnimation {
                    systemSplashDismissed = true
                    scheduleOnboardingIfVisible()
                }
            }
        }

        content.doOnPreDraw {
            content.postOnAnimation {
                contentDrawn = true
                scheduleOnboardingIfVisible()
            }
        }
    }

    override fun onStart() {
        super.onStart()
        activityStarted = true
        scheduleOnboardingIfVisible()
    }

    override fun onStop() {
        activityStarted = false
        handler.removeCallbacks(openOnboarding)
        super.onStop()
    }

    private fun scheduleOnboardingIfVisible() {
        handler.removeCallbacks(openOnboarding)
        if (activityStarted && contentDrawn && systemSplashDismissed) {
            // UI preview duration; real data loading has not been connected yet.
            handler.postDelayed(openOnboarding, 1_500L)
        }
    }
}

```

### ic_splash_placeholder.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_splash_placeholder.xml`

**Действие:** Создать новый XML-файл в папке res/drawable.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="288dp"
    android:height="288dp"
    android:viewportWidth="288"
    android:viewportHeight="288">
    <!-- Avoid a second, centered logo before the full Figma splash layout. -->
    <path
        android:fillColor="@android:color/transparent"
        android:pathData="M0,0 H288 V288 H0 Z" />
</vector>

```

### studyflow_splash_theme.xml

**Полный путь:** `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values-v31\studyflow_splash_theme.xml`

**Действие:** Открыть существующий файл и полностью заменить содержимое.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.StudyFlowApp.Splash" parent="Base.Theme.StudyFlowApp.Splash">
        <item name="android:windowSplashScreenBackground">@color/studyflow_blue_start</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/ic_splash_placeholder</item>
        <item name="android:windowSplashScreenAnimationDuration">0</item>
    </style>
</resources>

```

