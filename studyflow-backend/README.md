# StudyFlow: Django + JWT

Для размещения учебного сервера в интернете подготовлена отдельная конфигурация PythonAnywhere: см. `HOSTING.md`. Локальная конфигурация ниже продолжает работать как раньше.

Это локальный сервер авторизации для Android-приложения StudyFlowApp. Используются Django 5.2 LTS, Django REST Framework и Simple JWT. Установленные версии зафиксированы в `requirements.txt`.

## Как запустить на этом компьютере

Открой Terminal в Android Studio и выполни команды PowerShell:

```powershell
Set-Location -LiteralPath 'C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend'
& '.\.venv\Scripts\python.exe' manage.py runserver 127.0.0.1:8000
```

Оставь этот терминал открытым. Сервер должен работать, пока ты проверяешь вход в приложении. Если порт 8000 уже занят запущенным StudyFlow, второй сервер запускать не нужно. Остановить сервер в терминале: **Ctrl+C**.

На новом компьютере сначала выполни:

```powershell
python -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' bootstrap.py
& '.\.venv\Scripts\python.exe' manage.py migrate
& '.\.venv\Scripts\python.exe' manage.py runserver 127.0.0.1:8000
```

Также можно запустить `start-backend.ps1` из PowerShell. Он создаёт окружение при необходимости, сохраняет существующие ключи, применяет миграции и запускает сервер. Не нужно менять системную политику выполнения PowerShell: если запуск скриптов запрещён, используй команды выше.

## Подключение Android

Адрес debug-сборки по умолчанию — `http://10.0.2.2:8000/api/`. Он предназначен для эмулятора. На этом компьютере после настройки настоящего телефона в `gradle.properties` задано переопределение `STUDYFLOW_API_URL=http://127.0.0.1:8000/api/` для подключения по USB.

После переподключения телефона или перезапуска компьютера выполни в PowerShell `& 'C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\connect-phone.ps1'`. Скрипт при необходимости запускает Django и настраивает USB-перенаправление. Телефон должен оставаться подключённым. Подробная инструкция находится в соседней папке `phone-connection/Как-подключить-телефон.md`.

В Android Studio нажми **Run ▶**, открой регистрацию и создай свой аккаунт. Теперь произвольный email и пароль не откроют Home: вход проверяется сервером.

На Android 17 при первом локальном запросе приложение попросит разрешение **Nearby devices / Устройства поблизости**. Оно необходимо для обращения к локальному серверу и объявлено только в debug-сборке. Если отказать, приложение предложит открыть настройки или отменить действие.

Для телефона по USB выполни:

```powershell
& 'C:\Users\admin\AppData\Local\Android\Sdk\platform-tools\adb.exe' -s SERIAL reverse tcp:8000 tcp:8000
```

Заменить SERIAL на идентификатор телефона из `adb devices`. В файл `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\gradle.properties` добавь:

```properties
STUDYFLOW_API_URL=http://127.0.0.1:8000/api/
```

Пересобери приложение. Для возврата к обычному эмулятору удали эту строку. Переадресацию USB нужно повторять после переподключения устройства. При желании тот же способ работает с эмулятором.

## API

Все тела запросов и ответы — JSON. Указанные пути добавляются к адресу сервера.

| Метод | Путь | Назначение |
|---|---|---|
| POST | `/api/auth/register/` | Создание аккаунта; возвращает access, refresh и user |
| POST | `/api/auth/login/` | Вход по email и паролю; возвращает access, refresh и user |
| POST | `/api/auth/refresh/` | Обновление пары токенов |
| GET | `/api/auth/me/` | Профиль; нужен заголовок Authorization |
| POST | `/api/auth/logout/` | Отзыв refresh-токена |

Регистрация:

```json
{
  "email": "student@example.com",
  "full_name": "Test Student",
  "university": "Test University",
  "password": "ChooseYourOwnStrongPassword!",
  "terms_accepted": true
}
```

Вход:

```json
{"email":"student@example.com","password":"ChooseYourOwnStrongPassword!"}
```

Обновление или выход:

```json
{"refresh":"REFRESH_TOKEN_FROM_SERVER"}
```

Для профиля приложение добавляет:

```text
Authorization: Bearer ACCESS_TOKEN_FROM_SERVER
```

Access действует 5 минут, refresh — 7 дней. При обновлении refresh заменяется новым, а предыдущий заносится в список отозванных. При каждом успешном обновлении срок нового refresh снова составляет 7 дней. Выход отзывает refresh; уже выданный access остаётся действительным до своего истечения, максимум 5 минут. Android сразу удаляет локальные токены.

Пароль должен содержать минимум 8 символов. Дополнительно Django отклоняет распространённые пароли, пароли из одних цифр и слишком похожие на имя/email. Email, имя и университет обязательны; согласие проверяется сервером. Email нормализуется в нижний регистр и уникален без учёта регистра.

Статусы: **201** — аккаунт создан, **200** — успех, **400** — неправильные данные, **401** — неверные данные входа/токен, **429** — слишком много попыток. Лимиты: вход 10/мин, регистрация 5/мин, обновление и выход 30/мин. В локальном режиме они хранятся в памяти процесса; перед публичным запуском нужен общий cache и защита на уровне сервера.

## Что хранится и где

- `db.sqlite3`: аккаунты, хеши паролей, согласие и записи refresh-токенов. Пароли не сохраняются открытым текстом.
- `.local-settings.json`: локальные секреты Django и подписи JWT. Создаются случайно при первом `bootstrap.py`. Файл исключён из Git и архива исходников. Не удаляй его при обычном перезапуске: смена ключа сделает старые токены недействительными.
- Android: зашифрованная пара access/refresh в `noBackupFilesDir/auth-session.bin`; ключ AES-GCM находится в Android Keystore. Пароль приложение на диск не сохраняет. Секрет подписи JWT в APK отсутствует.
- При невозможности обновить сессию из-за истёкшего/отозванного refresh приложение возвращает на Login. При временном отсутствии сети токены сохраняются для повтора.
- При выходе без сети локальная сессия удаляется, но серверный refresh не может быть немедленно отозван; приложение сообщает об этом.

## Проверки и администрирование

```powershell
& '.\.venv\Scripts\python.exe' manage.py test accounts
& '.\.venv\Scripts\python.exe' manage.py check
```

Для административного доступа создай своего администратора (пароль вводится интерактивно):

```powershell
& '.\.venv\Scripts\python.exe' manage.py createsuperuser
```

После этого можно открыть `http://127.0.0.1:8000/admin/`. Общего пароля администратора в проекте нет.

Периодически удаляй истёкшие записи токенов командой:

```powershell
& '.\.venv\Scripts\python.exe' manage.py flushexpiredtokens
```

## Границы текущего этапа

Реально работают аккаунты, вход, профиль, JWT, обновление и выход. Карточки задач, даты, расписание и проценты Home пока остаются демонстрационными. Profile временно открывает диалог с данными аккаунта и кнопкой Log Out; отдельный дизайн профиля ещё не добавлялся. Восстановление пароля и подтверждение email пока не подключены.

Сервер запущен локально, в интернет не опубликован. Для публичного использования нужны HTTPS, production WSGI/ASGI-сервер, резервные копии базы, настройка общего cache и развёртывания. В production задать `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY`, `JWT_SIGNING_KEY`, `DJANGO_ALLOWED_HOSTS`. Для release APK задать Gradle-свойство `STUDYFLOW_RELEASE_API_URL=https://YOUR_DOMAIN/api/`. Без корректного HTTPS-адреса release-клиент не отправляет учётные данные. Локальный HTTP разрешён только debug-сборке и только для трёх указанных локальных адресов.

## Документация

- [Django: собственная модель пользователя](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/)
- [Simple JWT: подключение](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/getting_started.html)
- [Simple JWT: ротация и сроки токенов](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/settings.html)
- [Android Keystore](https://developer.android.com/privacy-and-security/keystore)
- [Android 17: локальная сеть](https://developer.android.com/privacy-and-security/local-network-permission)
