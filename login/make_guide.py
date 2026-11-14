from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET,zipfile
HERE=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=HERE/'StudyFlowApp-login'
files=sorted(p for p in PACKAGE.rglob('*') if p.is_file())
changed={str(p.relative_to(PACKAGE)) for p in files}
baseline=json.loads((HERE/'before.json').read_text())
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in files: assert digest(p)==digest(PROJECT/p.relative_to(PACKAGE)),str(p)
protected=[rel for rel in baseline if rel not in changed]
for rel in protected:assert digest(PROJECT/rel)==baseline[rel],rel
for p in files:
    if p.suffix=='.xml':ET.parse(p)
lint=ET.parse(PROJECT/'app/build/reports/lint-results-debug.xml')
errors=[n for n in lint.iter('issue') if n.get('severity') in ['Error','Fatal']]
warnings=[n for n in lint.iter('issue') if n.get('severity')=='Warning']
assert not errors
checks=json.loads((HERE/'verification.json').read_text())
assert checks['initial_email_unfocused'] and checks['small_screen_keyboard_field_visible']
guide=['''# StudyFlowApp — экран Login

## 1. Анализ дизайна

Экран собран по Login.svg и Brand mark.svg: белый фон, логотип 56×56 dp, заголовок Inter Bold 34 sp, подзаголовок, карточка формы 342×320 dp при ширине экрана 390 dp, два поля 52 dp, чекбокс, ссылка восстановления пароля, кнопка Log In и нижние ссылки. Цвета и шрифты переиспользованы из предыдущих экранов.

Верхняя строка состояния и нижняя полоса жестов принадлежат Android. Их значки, время и оттенок полосы могут отличаться от iOS-макета; второй набор системных значков не нарисован.

## 2. Какие файлы нужны

Изменения уже установлены в ваш проект. Вручную копировать код сейчас не требуется.

Из прежних файлов изменены только AndroidManifest.xml (регистрация LoginActivity) и OnboardingActivity.kt (переходы). MainActivity, splash и разметки предыдущих экранов сохранены.

Полный список файлов этого этапа:
''']
for p in files:
    rel=p.relative_to(PACKAGE);action='изменён' if str(rel) in baseline else 'создан'
    guide.append(f'- `{PROJECT/rel}` — {action}.')
guide.append('''
## 3. Пошаговая инструкция

1. Открой Android Studio и проект `C:\\Users\\admin\\AndroidStudioProjects\\StudyFlowApp`.
2. Вверху выбери конфигурацию **app** и свой эмулятор.
3. Нажми зелёный треугольник **Run**. Если приложение уже открыто, запуск через Run покажет начальную последовательность экранов.
4. После splash на любом onboarding нажми **Log In** или **Skip**. Также Login открывается по **Get Started** на последнем onboarding.
5. Нажми поле, чтобы открыть клавиатуру. Введи любой тестовый текст. Значок глаза показывает и скрывает введённый пароль; Remember me переключается.
6. **Log In** закрывает клавиатуру и остаётся на этом экране. Восстановление пароля и создание аккаунта пока дают только визуальную реакцию на касание. Их экраны добавим по следующим макетам.
7. Системная кнопка/жест «Назад» возвращает к тому onboarding, с которого открыт Login.

Адрес email и точки пароля из макета показаны как подсказки. Поля изначально пустые. Авторизация, запросы и сохранение учётных данных не добавлены; Remember me пока управляет только своим состоянием на экране.

Если нужно перенести этот этап в копию того же проекта: распакуй `StudyFlowApp-login.zip` и скопируй его папку `app` в корень проекта, объединив папки. Архив содержит только файлы этого этапа и требует ресурсы уже созданных экранов. Для двух заменяемых файлов сохранена резервная копия в папке `login/backup` рядом с этой инструкцией.

## 4. Готовый код

Ниже полный код каждого текстового файла. Если восстанавливаешь файл вручную: открой указанный путь, выдели содержимое целиком и вставь соответствующий код. Не заменяй другие файлы проекта.

Для нового XML в папке `res/layout`, `res/drawable` или `res/values`: нажми по папке правой кнопкой → **New → Layout Resource File / Drawable Resource File / Values Resource File**, укажи имя без `.xml`, затем переключись в **Code** и вставь полный код.

Для Kotlin: открой пакет `com.example.studyflowapp` в основной группе `kotlin+java` (без test/androidTest), выбери **New → Kotlin Class/File → File**, имя `LoginActivity`.

PNG-тени уже подготовлены по параметрам SVG. Их не нужно создавать как XML: скопируй готовые PNG из архива в папку `app/src/main/res/drawable-xxhdpi`. Если папки нет, создай её через **New → Android Resource Directory**, Resource type `drawable`, Density `XX-High Density`.
''')
for p in files:
    rel=p.relative_to(PACKAGE)
    guide.append(f'### Файл: `{PROJECT/rel}`\n')
    if p.suffix=='.png':
        guide.append('Действие: использовать готовый PNG из архива по этому же относительному пути.\n')
    else:
        guide.append('Действие: создать файл, если его нет, или полностью заменить его содержимое следующим кодом.\n')
        lang='kotlin' if p.suffix=='.kt' else 'xml'
        guide.append(f'```{lang}\n{p.read_text(encoding="utf-8").rstrip()}\n```\n')
guide.append(f'''## 5. Проверка

- `assembleDebug` и `lintDebug`: успешно, ошибок 0. Предупреждений {len(warnings)} — прежние замечания о ресурсах, размерах текста предыдущих экранов и доступной версии Gradle-плагина; новый экран не добавил предупреждений.
- Проверено в Android-эмуляторе API 37: переходы Log In / Skip / Get Started последнего шага и возврат назад.
- Проверены ввод тестового email и пароля, переключатель видимости, чекбокс и отсутствие перехода/авторизации после Log In.
- При 390×844 dp заголовок начинается в x=24, y=193; карточка — x=24, y=364.33; кнопка — x=44, y=612.33. Отличие от целых координат SVG связано с округлением метрик шрифта.
- Проверен небольшой экран 360×640 dp с размером текста 130%: доступна прокрутка, поле пароля полностью находится над клавиатурой.
- Настройки эмулятора восстановлены. Тестовые значения убраны повторным открытием экрана.
- {len(protected)} прежних файлов проверены по SHA-256 и не изменены. Runtime-проверка на API 24 отдельно не выполнялась; проект сохраняет minSdk 24.

Ожидаемый результат: белый экран входа как на макете, без автоматически открытой клавиатуры и без курсора в поле при первом открытии. На небольшом экране содержимое можно прокрутить.

Скриншоты: `Login-390x844.png`, `Login-emulator.png`, `Login-small-font130.png`, `Login-small-keyboard.png`. Подробности проверок — `verification.json`.
''')
(HERE/'Login-инструкция-и-код.md').write_text('\n\n'.join(guide),encoding='utf-8')
with zipfile.ZipFile(HERE/'StudyFlowApp-login.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for p in files:archive.write(p,p.relative_to(PACKAGE))
print(f'Guide + incremental archive ready: {len(files)} files, {len(protected)} existing files preserved, {len(warnings)} warnings, 0 errors.')
