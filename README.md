# StudyFlow

Android-приложение для учёбы и Django API. Передача проекта: 14 ноября 2026 года.

## С чего начать

1. Клонируйте этот репозиторий в папку с коротким путём латиницей, например `C:\Projects\StudyFlow`.
2. В Android Studio откройте **android**, дождитесь Gradle Sync и установите предложенные компоненты SDK.
3. Используйте встроенный JDK Android Studio. Версии проекта: Gradle 9.6.0, Android Gradle Plugin 9.4.1, compileSdk/targetSdk 37, minSdk 24. Все версии зависимостей сохранены в исходниках; Gradle Wrapper включён.
4. Выберите эмулятор или телефон и нажмите Run. В `android/gradle.properties` уже настроен HTTPS API: `https://dileeeekk.pythonanywhere.com/api/`.
5. Зарегистрируйте свой аккаунт. Проверьте создание задачи, занятия, заметки, выход и повторный вход.

Работа облачного сервера зависит от хостинга и его владельца. GitHub предоставляет исходники, но не доступ к панели PythonAnywhere. Для независимой работы запустите свой сервер по инструкции ниже или разверните его по `studyflow-backend/HOSTING.md`.

## Структура

| Папка | Назначение |
| --- | --- |
| `android` | Полный актуальный Android-проект; продолжать разработку здесь |
| `studyflow-backend` | Полный сервер: accounts, planner, config, миграции и тесты |
| `home-flow` | Описание последнего обновления планера, скриншоты и материалы проверок |
| Остальные папки | Исторические изменения, резервные копии исходников, архивы, изображения и инструкции |

Старые архивы и инструкции отражают состояние соответствующего этапа. Не накладывайте старые изменения поверх `android`. Установочные и проверочные скрипты прошлых этапов могут содержать абсолютные пути исходного компьютера; они сохранены для справки и не нужны для обычного запуска.

## Что уже работает

- Заставка, onboarding, регистрация, вход, JWT-сессии, обновление токенов и выход.
- Главная страница с данными пользователя и пустым состоянием нового аккаунта.
- Создание, редактирование, удаление и завершение задач.
- Занятия на конкретные даты, заметки, цель и ручная запись времени учёбы.
- Хранение данных планера на сервере отдельно для каждого аккаунта.

Ещё не реализованы офлайн-синхронизация, системные push-уведомления, таймер учёбы, повторяющееся расписание, восстановление пароля и подтверждение email. Profile пока открывает диалог аккаунта. Подробности интерфейса — в `home-flow/README.md`.

## Собственный локальный сервер (Windows PowerShell)

Установите Python; на исходном компьютере используется Python 3.13. Из корня репозитория:

```powershell
cd studyflow-backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe bootstrap.py
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Терминал оставьте открытым. Ключи и пустая база создаются локально. Существующие облачные аккаунты не переносятся: зарегистрируйте тестовый аккаунт на своём сервере.

Для Android Emulator замените значение в `android/gradle.properties` и пересоберите debug-приложение:

```properties
STUDYFLOW_API_URL=http://10.0.2.2:8000/api/
```

Для физического телефона по USB используйте `STUDYFLOW_API_URL=http://127.0.0.1:8000/api/` и выполните `adb reverse tcp:8000 tcp:8000` (adb находится в Android SDK/platform-tools). После переподключения USB повторите команду. На Android 17 разрешите локальный сетевой доступ, если приложение его запросит.

Для своего облачного сервера настройте оба свойства на его HTTPS-адрес с окончанием `/api/`:

```properties
STUDYFLOW_API_URL=https://YOUR_DOMAIN/api/
STUDYFLOW_RELEASE_API_URL=https://YOUR_DOMAIN/api/
```

## Проверки

Из `studyflow-backend`:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test accounts planner config
```

Из `android`, с настроенным Android SDK и JDK:

```powershell
.\gradlew.bat assembleDebug lintDebug
```

Тест `JwtIntegrationTest` требует локального сервера и тестового устройства; не запускайте его против чужих реальных аккаунтов. Исторические JSON-отчёты относятся к прошлым проверкам и не заменяют повторную проверку после изменений.

## Где менять код

- Android: `android/app/src/main/java/com/example/studyflowapp/`.
- Авторизация: подпапка `auth`, сервер `studyflow-backend/accounts`.
- Планер: подпапка `planner`, сервер `studyflow-backend/planner`.
- Разметка и оформление: `android/app/src/main/res/`.
- API маршруты: `studyflow-backend/config/urls.py`.
- API авторизации: `/api/auth/register/`, `/api/auth/login/`, `/api/auth/refresh/`, `/api/auth/me/`, `/api/auth/logout/`.
- Планер: `GET /api/planner/` и `POST /api/planner/`; формат операций см. в `planner/serializers.py`, `planner/views.py` и тестах.
- Проверка сервера: `GET /api/health/`.

## Продолжение работы через Git

Перед работой выполните `git pull`. После изменений выполните `git add .`, `git commit -m "Describe changes"`, `git push`. Для отправки изменений нужен принятый доступ участника репозитория.

В репозиторий не включаются базы с аккаунтами, секреты сервера, ключи подписи APK, виртуальные окружения и кэши. Они перечислены в `.gitignore`. Android Studio создаст собственный `local.properties` с путём к SDK. Секреты существующего хостинга и доступ к его панели передаются отдельно, если требуется сопровождение именно этого сервера.
