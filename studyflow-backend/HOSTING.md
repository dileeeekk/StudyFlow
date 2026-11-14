# Бесплатный учебный сервер PythonAnywhere

Этот вариант предназначен для небольшого учебного проекта. Сервер работает на хостинге независимо от компьютера. Бесплатное веб-приложение требуется продлевать в панели хостинга; текущий срок — один месяц. SQLite доступна на бесплатном тарифе, но для реальной нагрузки провайдер рекомендует другую базу.

Официальные источники, проверены 07.11.2026:
- https://help.pythonanywhere.com/pages/FreeAccountsFeatures/
- https://help.pythonanywhere.com/pages/KindsOfDatabases
- https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
- https://help.pythonanywhere.com/pages/StaticFiles/

## Порядок размещения для сопровождающего разработчика

1. Пользователь самостоятельно создаёт бесплатный аккаунт, принимает условия сервиса и подтверждает почту, если сервис попросит.
2. Загрузить `StudyFlow-hosting.zip` через Files в домашнюю папку. Архив содержит только исходники, без локальных пользователей, паролей, токенов и ключей.
3. В Bash-консоли хостинга распаковать архив в домашнюю папку. При первом запуске:

```bash
cd ~
unzip StudyFlow-hosting.zip
python3.13 -m venv ~/.virtualenvs/studyflow
source ~/.virtualenvs/studyflow/bin/activate
cd ~/studyflow-backend
python -m pip install -r requirements.txt
python deploy_pythonanywhere.py USERNAME.pythonanywhere.com
```

Заменить USERNAME фактическим именем из панели аккаунта. Если аккаунт в регионе EU, использовать точный домен из панели, включая `.eu.`. Версия Python в виртуальном окружении и Web должна совпадать; если 3.13 не предлагается, выбрать доступную версию >=3.10, совместимую с Django 5.2.

4. Web → Add a new web app → бесплатный домен → Manual configuration → соответствующая версия Python.
5. Virtualenv: `/home/USERNAME/.virtualenvs/studyflow`.
6. Source code: `/home/USERNAME/studyflow-backend`.
7. В WSGI configuration file вставить содержимое `pythonanywhere_wsgi.py` из проекта.
8. Static files: URL `/static/`, Directory `/home/USERNAME/studyflow-backend/staticfiles`. Не добавлять маршруты ко всему домашнему каталогу, `.studyflow` или исходникам.
9. Reload. Проверить `https://USERNAME.pythonanywhere.com/api/health/`: ожидается `{"status":"ok"}`. Проверить `/api/auth/me/`: без токена ожидается HTTP 401.
10. Проверить учебным аккаунтом регистрацию, вход, профиль, обновление и отзыв токена через HTTPS. Не печатать пароль или токены в отчёте.

## Хранение данных

`~/.studyflow/server.json` содержит уникальные ключи сервера; `~/.studyflow/db.sqlite3` — облачные аккаунты. Они расположены вне исходников и не заменяются при обновлении кода. Повторный запуск setup_hosting.py сохраняет существующие ключи. Копировать эти файлы в публичные каталоги или репозиторий нельзя. Резервную копию базы создавать средствами SQLite backup, ключи хранить отдельно в защищённом месте.

Облачная база первоначально пустая: локальные аккаунты с компьютера не загружаются автоматически. Для демонстрации можно зарегистрироваться заново. Если требуется перенос существующих пользователей, отдельно согласовать и выполнить перенос без публикации базы в архиве.

Перед повторным развёртыванием проверить содержимое архива, сохранить резервную копию исходников и обновлять только их. Не удалять `~/.studyflow` и не создавать новый серверный ключ при каждом релизе. Периодически запускать `python manage_hosting.py flushexpiredtokens` для очистки истёкших записей JWT.

## Подключение Android — только после проверки сервера

В `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\gradle.properties` заменить локальный STUDYFLOW_API_URL и добавить release URL:

```properties
STUDYFLOW_API_URL=https://USERNAME.pythonanywhere.com/api/
STUDYFLOW_RELEASE_API_URL=https://USERNAME.pythonanywhere.com/api/
```

Собрать assembleDebug, обновить APK через adb install -r. Проверить регистрацию и вход на телефоне после отключения USB и на мобильном интернете. Смена адреса API требует повторного входа: локальные токены намеренно привязаны к прежнему серверу. Пока фактический URL не получен и сервер не проверен, локальный адрес приложения остаётся прежним.

## Выполненные локальные проверки

- `manage.py test accounts config`: 11 тестов успешно.
- Изолированная конфигурация хостинга: `check --deploy --fail-level WARNING` без замечаний.
- Временная база: регистрация, доступ к профилю, ротация и отзыв JWT, ограничение попыток входа, редирект HTTP → HTTPS.
- Локальная база пользователя и ключи проверены по хешам, не изменены.

Реальный запуск в облаке и проверка без USB выполняются после входа в аккаунт хостинга.
