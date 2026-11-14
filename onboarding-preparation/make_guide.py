from pathlib import Path
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
PACKAGE = HERE/'StudyFlowApp-onboarding'
PROJECT = Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
files = sorted(p for p in PACKAGE.rglob('*') if p.is_file())
checks = json.loads((HERE/'verification.json').read_text(encoding='utf-8'))
lint = ET.parse(PROJECT/'app/build/reports/lint-results-debug.xml')
issues = lint.findall('issue')
errors = [i for i in issues if i.get('severity') in ('Error','Fatal')]
warnings = [i for i in issues if i.get('severity') == 'Warning']
assert not errors
assert all(checks['settings_restored'].values())
assert checks['small_screen_cta_visible'] and checks['small_screen_login_visible']

for p in files:
    assert p.read_bytes() == (PROJECT/p.relative_to(PACKAGE)).read_bytes(), p
    if p.suffix == '.xml':
        ET.parse(p)

previous = HERE.parent/'splash-preparation/StudyFlowApp-splash'
preserved = []
for p in previous.rglob('*'):
    if p.is_file() and p.suffix != '.kt' and p.name != 'AndroidManifest.xml':
        rel = p.relative_to(previous)
        assert p.read_bytes() == (PROJECT/rel).read_bytes(), f'Splash resource changed: {rel}'
        preserved.append(str(rel))

body = ['''# StudyFlow — Onboarding «Track Every Deadline»

## 1. Анализ дизайна

Экран перенесён из вашего SVG 390 × 844. Использована ваша PNG-иллюстрация
1026 × 840 без изменений. Текст, кнопки, карточка-пример задания и индикаторы
созданы отдельными Android Views в XML.

| Элемент | Параметры макета |
|---|---|
| Боковые поля | 24dp |
| Иллюстрация с подложкой | 342 × 332, радиус 30 |
| Иллюстрация внутри карточки | 342 × 280 |
| Полупрозрачная карточка задания | 314 × 60, радиус 18 |
| Плашка над заголовком | 207 × 22, радиус 11 |
| Заголовок | Inter Bold, 32sp |
| Описание | Inter Regular, 14sp |
| Основной текст | #172443 |
| Вторичный текст | #66728B |
| Кнопка | #4564ED, высота 52dp, радиус 14 |

Верхний текст — Inter Bold 16sp; Skip — Inter Medium 13sp; Get Started —
Inter SemiBold 14sp. Ранее добавленные Inter Regular, Medium и Bold используются
повторно; добавлен только SemiBold. Синяя тень кнопки подготовлена из параметров
SVG: смещение 8, Gaussian blur sigma 10, непрозрачность 48/255.

Разметка Splash и его ресурсы сохранены без изменений. Добавлен временный
переход: через 1,2 секунды показа Splash открывается onboarding. При уходе
приложения в фон ожидающий переход отменяется. Возврат кнопкой Back из
onboarding закрывает этот экран; заставка не остаётся под ним в стеке.

Skip, Get Started и Log In пока дают только реакцию на нажатие. Переходы
к регистрации, авторизации и остальным onboarding-экранам ещё не подключены,
так как соответствующих реализованных экранов пока нет. Данные не сохраняются.

## 2. Какие файлы нужны

Папка проекта: `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`.
Из существующих файлов изменены только `MainActivity.kt` и `AndroidManifest.xml`.
Все остальные файлы ниже — новые. Gradle и архитектура приложения не изменены.

''']

for p in files:
    rel = p.relative_to(PACKAGE)
    body.append(f'- [{rel.as_posix()}](<{(PROJECT/rel).as_posix()}>)\n')

body.append('''
## 3. Пошаговая инструкция

Файлы уже добавлены в проект. Повторно копировать код не нужно.

1. Откройте **StudyFlowApp** в Android Studio.
2. В верхней панели выберите **app** и **Medium Phone API 37.0**.
3. Нажмите зелёную кнопку **Run ▶**.
4. После системной заставки отобразится готовый Splash, затем новый onboarding.
5. Для изучения XML откройте **app → res → layout → activity_onboarding.xml**.
6. Для просмотра разметки рядом с кодом выберите **Split**.
7. Kotlin-код нового экрана находится в **app → kotlin+java →
   com.example.studyflowapp → OnboardingActivity**.

На небольшом экране или при увеличенном шрифте прокрутите страницу вверх,
чтобы добраться до Get Started и Log In. На размере макета всё помещается
без прокрутки. Прокрутка не добавляет новых видимых элементов интерфейса.

Для ручного восстановления этапа используйте архив `StudyFlowApp-onboarding.zip`.
Это дополнение к уже готовому проекту со Splash, а не отдельный Android-проект.
В архиве папка `app` соответствует папке `app` вашего проекта.

Kotlin-файлы создаются как **Kotlin Class/File**, XML — как **XML Resource File**
в указанной папке. Для бинарных ресурсов скопируйте готовые файлы из архива:
`inter_semibold.ttf` в `res/font`, обе PNG в `res/drawable-xxhdpi`.
XML-ресурсы в `values` создаются как **Values Resource File**.
Для `MainActivity.kt` и `AndroidManifest.xml` используйте полную замену содержимого
версиями ниже; остальные файлы создайте с указанными именами.

## 4. Готовый код

''')

for p in files:
    if p.suffix not in {'.kt','.xml'}:
        continue
    rel = p.relative_to(PACKAGE)
    language = 'kotlin' if p.suffix == '.kt' else 'xml'
    action = 'Заменить содержимое существующего файла.' if p.name in ('MainActivity.kt','AndroidManifest.xml') else 'Создать новый файл и вставить весь код.'
    body.append(f'### {p.name}\n\n**Файл:** `{PROJECT/rel}`\n\n**Действие:** {action}\n\n')
    body.append(f'```{language}\n{p.read_text(encoding="utf-8")}\n```\n\n')

body.append(f'''## 5. Проверка

- `assembleDebug` и `lintDebug` завершились успешно.
- Ошибок Lint: **{len(errors)}**. Предупреждений: **{len(warnings)}**.
- Запуск проверен на эмуляторе API 37; Splash автоматически открывает onboarding.
- При размере 390 × 844dp карточка занимает точные координаты SVG:
  x = 24, y = 116, ширина = 342, высота = 332.
- Проверен экран 360 × 640dp со шрифтом 130%: кнопка и Log In доступны после прокрутки.
- Нажатие Get Started оставляет пользователя на onboarding, как запланировано на этом этапе.
- Исходные размер, плотность и масштаб текста эмулятора восстановлены после проверки.
- Сверены {len(preserved)} файлов ресурсов Splash: их содержимое не изменилось.

Отдельного запуска на Android 7 не было; minSdk 24 проверен сборкой и Lint.
Скругление иллюстрации включается через Kotlin API, доступный на этой версии Android.

Предупреждения:

''')
for issue in warnings:
    body.append(f'- `{issue.get("id")}`: {issue.get("message")}\n')

body.append('''
Размеры 10sp в подписи иллюстрации и плашке сохранены из вашего макета.
Lint рекомендует более крупный текст, но самовольно менять дизайн я не стал.
Остальные предупреждения относятся к ресурсам и версии инструментов проекта.

Снимки рядом с этой инструкцией:

- `StudyFlow-Onboarding-emulator.png` — обычный размер вашего эмулятора.
- `Onboarding-390x844.png` — сравнение с макетом при 390 × 844dp, снимок в масштабе 3×.
- `Onboarding-small-font130.png` — небольшой экран с увеличенным текстом после прокрутки.

Время, батарея и нижняя жестовая полоска отображаются самой системой Android.
Они отличаются от нарисованных системных панелей iPhone в Figma.

Источник шрифта: [Inter 3.19](https://github.com/rsms/inter/releases/tag/v3.19).
Лицензия уже находится в `app/src/main/assets/licenses/inter_ofl.txt` со стадии Splash.
Основная кнопка использует существующий [MaterialButton](https://developer.android.com/reference/com/google/android/material/button/MaterialButton)
из зависимости Material проекта. Новых библиотек не установлено.
''')

guide = HERE/'StudyFlow-Onboarding-инструкция.md'
guide.write_text(''.join(body),encoding='utf-8')
with zipfile.ZipFile(HERE/'StudyFlowApp-onboarding.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p,p.relative_to(PACKAGE))
    z.write(guide,guide.name)

summary = {'installed_files':len(files),'lint_errors':len(errors),'lint_warnings':len(warnings),'splash_resources_unchanged':len(preserved),'archive_bytes':(HERE/'StudyFlowApp-onboarding.zip').stat().st_size}
(HERE/'delivery-check.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary))
