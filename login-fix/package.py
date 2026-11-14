from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=ROOT/'StudyFlowApp-login-fix'
files=sorted(p for p in PACKAGE.rglob('*') if p.is_file())
changed={str(p.relative_to(PACKAGE)) for p in files}
before=json.loads((ROOT/'before.json').read_text())
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in files:assert digest(p)==digest(PROJECT/p.relative_to(PACKAGE))
for rel,sha in before.items():
    if rel not in changed:assert digest(PROJECT/rel)==sha,rel
lint=ET.parse(PROJECT/'app/build/reports/lint-results-debug.xml')
assert not [i for i in lint.iter('issue') if i.get('severity') in ['Error','Fatal']]
checks=json.loads((ROOT/'verification.json').read_text())
assert len(checks)==4 and all(checks.values())
guide=['''# Исправление полей Login

Изменения уже установлены в проект StudyFlowApp; вручную вставлять код не нужно.

## Что исправлено

Удалены hint-подсказки email и пароля: при новом открытии оба поля пусты. Названия Email address и Password над полями сохранены.

В Gboard на эмуляторе был выключен показ экранной клавиатуры при подключённой физической клавиатуре. Вместо букв появлялась боковая панель. В настройках Gboard → Physical keyboard включён Show on-screen keyboard. Также включён системный показ клавиатуры при подключённой физической клавиатуре. Это настройка эмулятора; она не переносится вместе с APK на другое устройство. В коде формы нажатие на любое поле явно запрашивает экранную клавиатуру. Временные изменения для проверки гипотезы о рукописном вводе убраны.

## Как проверить

1. В Android Studio открой проект `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`.
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
''']
for p in files:
    rel=p.relative_to(PACKAGE);lang='kotlin' if p.suffix=='.kt' else 'xml'
    guide.append(f'### `{PROJECT/rel}`\n\n```{lang}\n{p.read_text(encoding="utf-8").rstrip()}\n```')
(ROOT/'Исправление-Login-инструкция.md').write_text('\n\n'.join(guide),encoding='utf-8')
with zipfile.ZipFile(ROOT/'StudyFlowApp-login-fix.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(PACKAGE))
print(f'3 files verified; {len(before)-3} existing files preserved. Guide and archive ready.')
