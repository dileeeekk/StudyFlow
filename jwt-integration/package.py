from pathlib import Path
import hashlib,json,os,zipfile,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
BACKEND=ROOT.parent/'studyflow-backend'
STAGE=ROOT/'android'
files=sorted(p for p in STAGE.rglob('*') if p.is_file())
before=json.loads((ROOT/'before.json').read_text())
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed={str(p.relative_to(STAGE)) for p in files}
for p in files:assert digest(p)==digest(PROJECT/p.relative_to(STAGE)),str(p)
for rel,sha in before.items():
    if rel not in changed:assert digest(PROJECT/rel)==sha,rel
assert not any('/res/layout/' in str(p).replace('\\','/') for p in files)
assert 'OK (1 test)' in (ROOT/'android-test-result.txt').read_text(encoding='utf-8-sig')
assert all(json.loads((ROOT/'ui-verification.json').read_text()).values())
assert all(json.loads((ROOT/'offline-verification.json').read_text()).values())
lint=ET.parse(PROJECT/'app/build/reports/lint-results-debug.xml')
assert not [n for n in lint.iter('issue') if n.get('severity') in ['Error','Fatal']]
backend_files=[]
for directory,dirs,names in os.walk(BACKEND):
    dirs[:]=[d for d in dirs if d not in ['.venv','__pycache__','.git']]
    for name in names:
        p=Path(directory)/name
        if p.suffix in ['.py','.txt','.md','.ps1'] or p.name=='.gitignore':backend_files.append(p)
backend_files.sort()
guide=['''# StudyFlow — Django и JWT

Код уже добавлен в существующий Android-проект. Django-бэкенд создан в отдельной папке. Переносить код вручную на этом компьютере не требуется.

## 1. Что теперь работает

Login и Register отправляют данные в Django и переходят на Home только после успешного ответа. Django хранит аккаунты и хеши паролей в SQLite. Сервер выдаёт JWT access на 5 минут и refresh на 7 дней. Android использует access для защищённого профиля, а при ответе 401 один раз обновляет пару токенов и повторяет запрос. Если refresh недействителен, приложение очищает сессию и возвращает Login. При временной недоступности сервера сессия сохраняется и доступна кнопка Try again.

Токены зашифрованы AES-GCM; ключ находится в Android Keystore, файл не включается в резервное копирование. Пароль на устройстве не сохраняется. После перезапуска приложения действующая сессия восстанавливается через защищённый запрос к серверу. Имя приветствия берётся из аккаунта. Вкладка Profile временно открывает данные аккаунта и кнопку Log Out. Выход отзывает refresh и удаляет локальные токены.

XML-разметка существующих экранов, изображения и шрифты не изменялись. Даты, задачи, расписание и проценты на Home пока взяты из макета. Забытый пароль и подтверждение email ещё не подключены. Сервер локальный; публичное развёртывание не выполнялось.

## 2. Где находятся файлы

- Android: `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`.
- Django: `C:\\Users\\admin\\OneDrive\\Documents\\ChatGPT\\Приложение StudyFlow\\studyflow-backend`.
- Резервные копии изменённых Android-файлов: папка `backup` рядом с этой инструкцией.
- Архив `StudyFlow-JWT.zip`: папка `android` содержит только дополнения и изменения Android; папка `studyflow-backend` — исходный код сервера. База, секреты и виртуальное окружение в архив не включены.

## 3. Пошаговый запуск

1. Сервер оставлен работающим локально после проверки. Если компьютер перезапущен или сервер остановлен, открой **Terminal** в Android Studio и выполни:

```powershell
Set-Location -LiteralPath 'C:\\Users\\admin\\OneDrive\\Documents\\ChatGPT\\Приложение StudyFlow\\studyflow-backend'
& '.\\.venv\\Scripts\\python.exe' manage.py runserver 127.0.0.1:8000
```

2. Оставь терминал с сервером открытым. Если указано, что порт уже занят, проверь, не работает ли уже StudyFlow-сервер; второй экземпляр не нужен.
3. В Android Studio открой существующий **StudyFlowApp**, выбери **app**, свой эмулятор и нажми **Run ▶**.
4. Открой **Create an account**. Введи имя, email, университет и свой пароль. Нужны минимум 8 символов; Django также отклоняет очень простые, полностью цифровые и похожие на имя/email пароли. Установи согласие и нажми **Create Account**.
5. Если Android 17 запросит доступ к устройствам поблизости, разреши его для соединения с локальным тестовым сервером. В release-сборке это разрешение отсутствует.
6. Должен открыться Home с твоим именем. **Profile → Log Out** возвращает пустой Login. Теперь войди с теми же email и паролем. Неверный пароль должен показать ошибку.

Полная настройка нового компьютера, USB-телефона, адреса API, административного доступа и release-сборки находится в `studyflow-backend/README.md`.

## 4. Файлы и готовый код

Ниже приведены полные версии всех добавленных и изменённых файлов. При ручном переносе замени содержимое существующих файлов полностью. Для новых файлов создай указанные папки и файлы с точно такими именами. Kotlin-файлы создаются через **New → Kotlin Class/File → File**. XML — через **New → Android Resource File**, тип соответствует папке `res/xml` или `res/values`. Файлы Python и PowerShell — обычные текстовые файлы с расширениями `.py` и `.ps1`. Папка `src/debug` применяется только к debug-сборке, `src/androidTest` — к тестам на устройстве.
''']
for p in files:
    rel=p.relative_to(STAGE)
    action='Изменить существующий файл' if str(rel) in before else 'Создать файл'
    language='kotlin' if p.suffix in ['.kt','.kts'] else 'xml'
    guide.append(f'### `{PROJECT/rel}`\n\nДействие: {action}.\n\n```{language}\n{p.read_text(encoding="utf-8").rstrip()}\n```')
for p in backend_files:
    if p.suffix=='.md':continue
    language={'.py':'python','.ps1':'powershell'}.get(p.suffix,'text')
    guide.append(f'### `{p}`\n\nДействие: создать файл.\n\n```{language}\n{p.read_text(encoding="utf-8-sig").rstrip()}\n```')
guide.append('''## 5. Результаты проверки

- Django: 8 тестов прошли — создание аккаунта, хеширование пароля, обязательные поля и согласие, повторный email, вход, защищённый профиль, просроченный/изменённый access, ротация и отзыв refresh, неактивный пользователь, лимит попыток.
- Android: assembleDebug, assembleDebugAndroidTest и lintDebug прошли; ошибок Lint нет. Манифест release проверен отдельно: локальное сетевое разрешение и HTTP-конфигурация debug туда не попадают.
- Интеграционный тест в эмуляторе: настоящий Django, шифрование файла токенов, четыре одновременных запроса после недействительного access, ротация refresh, отказ при повторном использовании старого refresh, отзыв при выходе, неверный пароль, восстановление после повреждённого хранилища.
- Интерфейс: регистрация, имя на Home, сохранение сессии после остановки процесса, Profile / Log Out, пустые поля после выхода, ошибка неверного пароля и успешный вход.
- Недоступность сервера: сервер временно остановлен; токены сохранились. После запуска сервера Try again восстановила Home. Сервер снова работает, тестовая сессия на устройстве завершена.
- Все существующие XML-разметки сохранены без изменений.

Скриншоты проверки находятся рядом с инструкцией: JWT-register-home.png, JWT-account-dialog.png, JWT-invalid-password.png, JWT-offline-retry.png.

Для повторной проверки backend: из папки сервера выполни `.\\.venv\\Scripts\\python.exe manage.py test accounts`. Android-тест `JwtIntegrationTest` запускается из Android Studio при работающем локальном сервере и разрешённом доступе к локальной сети. Тест использует отдельный временный аккаунт `@example.com` и завершает сессию; запускай его на тестовом устройстве.

Ключевые особенности: после выхода уже выданный access остаётся действительным до истечения, максимум 5 минут; при выходе без сети Android удаляет локальные токены, но не может немедленно отозвать refresh на сервере. Публичный сервер и публикация приложения требуют отдельного этапа развёртывания, описанного в README.

Документация: [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/getting_started.html), [настройки JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/settings.html), [Android Keystore](https://developer.android.com/privacy-and-security/keystore).
''')
(ROOT/'JWT-инструкция-и-код.md').write_text('\n\n'.join(guide),encoding='utf-8')
with zipfile.ZipFile(ROOT/'StudyFlow-JWT.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,Path('android')/p.relative_to(STAGE))
    for p in backend_files:z.write(p,Path('studyflow-backend')/p.relative_to(BACKEND))
with zipfile.ZipFile(ROOT/'StudyFlow-JWT.zip') as z:
    assert not any('/.venv/' in n or n.endswith(('.sqlite3','.log','.local-settings.json')) for n in z.namelist())
summary={'android_files':len(files),'existing_android_files_changed':len(changed.intersection(before)),
         'existing_files_preserved':len(before)-len(changed.intersection(before)),
         'backend_source_files':len(backend_files),'layouts_unchanged':True,'archive_excludes_secrets_and_database':True}
(ROOT/'delivery-verification.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary))
