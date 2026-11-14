# Иконка StudyFlow

Иконка уже добавлена в проект и обновлена на подключённом телефоне. Повторно вставлять код не требуется.

Использован существующий контур книги с галочкой из ic_studyflow_logo.xml и цвета заставки: #273D86, #4969E8, #9672D6.

## Какие файлы изменены

- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_launcher_background.xml`
- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_launcher_foreground.xml`
- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\mipmap-anydpi\ic_launcher.xml`
- `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\mipmap-anydpi\ic_launcher_round.xml`

Первые два drawable — фон и белый знак. Файлы mipmap-anydpi — варианты для Android 7. Существующие mipmap-anydpi-v26/ic_launcher.xml и ic_launcher_round.xml уже подключают фон, знак и монохромный слой для новых версий Android. В AndroidManifest.xml ссылки на иконки уже были настроены.

Системная заставка использует отдельный ресурс, поэтому её настройка не менялась.

## Проверка

1. На телефоне открой список приложений и найди StudyFlowApp.
2. Иконка должна показывать белую книгу с галочкой на синем градиентном фоне.
3. Нажми на иконку для запуска приложения.
4. Для последующих сборок в Android Studio выбери конфигурацию app, подключённый телефон и нажми Run ▶.

Сборка assembleDebug завершилась BUILD SUCCESSFUL. Установка обновления через adb install -r завершилась Success. Проверена упаковка обычного и адаптивного вариантов в APK. Автоматическая проверка хешей подтвердила изменение только четырёх указанных ресурсов.

Если в списке приложений осталась старая иконка, перезагрузи телефон. Удалять приложение для этого не нужно.

Форма и тематическая окраска адаптивной иконки определяются оболочкой телефона: [документация Android](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive).

## Полный код ресурсов

Ниже приведён код для справки. Все файлы уже находятся в проекте. Тип новых файлов — XML.

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_launcher_background.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" xmlns:aapt="http://schemas.android.com/aapt"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:pathData="M0,0 H108 V108 H0 Z">
        <aapt:attr name="android:fillColor">
            <gradient android:type="linear" android:startX="0" android:startY="0" android:endX="108" android:endY="108">
                <item android:offset="0" android:color="#273D86" />
                <item android:offset="0.55" android:color="#4969E8" />
                <item android:offset="1" android:color="#9672D6" />
            </gradient>
        </aapt:attr>
    </path>
</vector>

```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\drawable\ic_launcher_foreground.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" xmlns:aapt="http://schemas.android.com/aapt"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <group android:translateX="-51.600" android:translateY="-37.200" android:scaleX="1.2" android:scaleY="1.2">
        <path android:pathData="M87.9996 94V66M87.9996 94C87.9996 92.4087 87.3675 90.8826 86.2421 89.7574C85.1168 88.6321 83.5906 88 81.9992 88H69.9982C69.4677 88 68.959 87.7893 68.5839 87.4142C68.2088 87.0391 67.998 86.5304 67.998 86V60C67.998 59.4696 68.2088 58.9609 68.5839 58.5858C68.959 58.2107 69.4677 58 69.9982 58H79.999C82.1209 58 84.1559 58.8429 85.6563 60.3431C87.1567 61.8434 87.9996 63.8783 87.9996 66M87.9996 94C87.9996 92.4087 88.6318 90.8826 89.7571 89.7574C90.8825 88.6321 92.4087 88 94.0001 88H106.001C106.532 88 107.04 87.7893 107.415 87.4142C107.791 87.0391 108.001 86.5304 108.001 86V83.4M87.9996 66C87.9996 63.8783 88.8426 61.8434 90.343 60.3431C91.8434 58.8429 93.8784 58 96.0003 58H106.001C106.532 58 107.04 58.2107 107.415 58.5858C107.791 58.9609 108.001 59.4696 108.001 60V64M96.0003 76L100.001 80L108.001 72" android:fillColor="@android:color/transparent" android:strokeColor="#FFFFFF" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>

```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\mipmap-anydpi\ic_launcher.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" xmlns:aapt="http://schemas.android.com/aapt"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:pathData="M27,3 H81 Q105,3 105,27 V81 Q105,105 81,105 H27 Q3,105 3,81 V27 Q3,3 27,3 Z">
        <aapt:attr name="android:fillColor">
            <gradient android:type="linear" android:startX="0" android:startY="0" android:endX="108" android:endY="108">
                <item android:offset="0" android:color="#273D86" />
                <item android:offset="0.55" android:color="#4969E8" />
                <item android:offset="1" android:color="#9672D6" />
            </gradient>
        </aapt:attr>
    </path><group android:translateX="-86.800" android:translateY="-67.600" android:scaleX="1.6" android:scaleY="1.6">
        <path android:pathData="M87.9996 94V66M87.9996 94C87.9996 92.4087 87.3675 90.8826 86.2421 89.7574C85.1168 88.6321 83.5906 88 81.9992 88H69.9982C69.4677 88 68.959 87.7893 68.5839 87.4142C68.2088 87.0391 67.998 86.5304 67.998 86V60C67.998 59.4696 68.2088 58.9609 68.5839 58.5858C68.959 58.2107 69.4677 58 69.9982 58H79.999C82.1209 58 84.1559 58.8429 85.6563 60.3431C87.1567 61.8434 87.9996 63.8783 87.9996 66M87.9996 94C87.9996 92.4087 88.6318 90.8826 89.7571 89.7574C90.8825 88.6321 92.4087 88 94.0001 88H106.001C106.532 88 107.04 87.7893 107.415 87.4142C107.791 87.0391 108.001 86.5304 108.001 86V83.4M87.9996 66C87.9996 63.8783 88.8426 61.8434 90.343 60.3431C91.8434 58.8429 93.8784 58 96.0003 58H106.001C106.532 58 107.04 58.2107 107.415 58.5858C107.791 58.9609 108.001 59.4696 108.001 60V64M96.0003 76L100.001 80L108.001 72" android:fillColor="@android:color/transparent" android:strokeColor="#FFFFFF" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>

```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\mipmap-anydpi\ic_launcher_round.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" xmlns:aapt="http://schemas.android.com/aapt"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:pathData="M54,3 A51,51 0,1 1,54,105 A51,51 0,1 1,54,3 Z">
        <aapt:attr name="android:fillColor">
            <gradient android:type="linear" android:startX="0" android:startY="0" android:endX="108" android:endY="108">
                <item android:offset="0" android:color="#273D86" />
                <item android:offset="0.55" android:color="#4969E8" />
                <item android:offset="1" android:color="#9672D6" />
            </gradient>
        </aapt:attr>
    </path><group android:translateX="-86.800" android:translateY="-67.600" android:scaleX="1.6" android:scaleY="1.6">
        <path android:pathData="M87.9996 94V66M87.9996 94C87.9996 92.4087 87.3675 90.8826 86.2421 89.7574C85.1168 88.6321 83.5906 88 81.9992 88H69.9982C69.4677 88 68.959 87.7893 68.5839 87.4142C68.2088 87.0391 67.998 86.5304 67.998 86V60C67.998 59.4696 68.2088 58.9609 68.5839 58.5858C68.959 58.2107 69.4677 58 69.9982 58H79.999C82.1209 58 84.1559 58.8429 85.6563 60.3431C87.1567 61.8434 87.9996 63.8783 87.9996 66M87.9996 94C87.9996 92.4087 88.6318 90.8826 89.7571 89.7574C90.8825 88.6321 92.4087 88 94.0001 88H106.001C106.532 88 107.04 87.7893 107.415 87.4142C107.791 87.0391 108.001 86.5304 108.001 86V83.4M87.9996 66C87.9996 63.8783 88.8426 61.8434 90.343 60.3431C91.8434 58.8429 93.8784 58 96.0003 58H106.001C106.532 58 107.04 58.2107 107.415 58.5858C107.791 58.9609 108.001 59.4696 108.001 60V64M96.0003 76L100.001 80L108.001 72" android:fillColor="@android:color/transparent" android:strokeColor="#FFFFFF" android:strokeWidth="1" android:strokeLineCap="round" android:strokeLineJoin="round" />
    </group>
</vector>

```

